# 02 — Deep-Dive Report: AI phân loại & điều hướng phản ánh cư dân Vinhomes

**Dự án:** Vinhomes Resident Smart Triage

**Mục tiêu:** Tự động hiểu, phân loại và chuyển đúng phản ánh của cư dân từ App Vinhomes Resident tới ban quản lý (BQL) tòa nhà hoặc đội chuyên môn phù hợp, đồng thời không bỏ sót các tình huống khẩn cấp.

---

# Phase 3 — DEEP-DIVE

## 3.1. Current-State Workflow

Hiện tại, phản ánh được cư dân gửi dưới dạng văn bản tự do, có thể kèm ảnh và thông tin căn hộ/khu vực. Nhân viên CSKH đọc từng ticket, tra cứu tòa nhà, xác định loại việc và chuyển đến đội phụ trách.

```text
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ 1. Cư dân gửi    │ -> │ 2. CSKH đọc      │ -> │ 3. CSKH xác định │
│ phản ánh trên app│    │ mô tả/ảnh, tra   │    │ loại sự cố và    │
│                  │    │ cứu tòa nhà      │    │ mức ưu tiên      │
│ ⏱ ~1 phút        │    │ ⏱ ~3 phút  🔴    │    │ ⏱ ~2 phút  🔴    │
└──────────────────┘    └──────────────────┘    └──────────────────┘
                                                           │
                                                           v
┌──────────────────┐    ┌──────────────────┐
│ 5. BQL/đội xử lý │ <- │ 4. CSKH chuyển   │
│ cập nhật tiến độ │    │ ticket đúng queue│
│ cho cư dân       │    │ ⏱ ~2 phút  🔴    │
└──────────────────┘    └──────────────────┘

🔴 Bottleneck: các bước đọc hiểu, phân loại và định tuyến.
⏱ Thời gian phân luồng hiện tại: khoảng 5–8 phút/ticket.
```

### Các điểm nghẽn chính

1. **Nội dung không chuẩn hóa:** Cư dân có thể viết tắt, thiếu dấu, mô tả chung chung (“nước chảy ngoài hành lang”) hoặc nêu nhiều vấn đề trong một ticket.
2. **Tuyến xử lý phụ thuộc ngữ cảnh:** Cùng một lỗi “hỏng đèn” nhưng cần biết vị trí là căn hộ, hành lang, hầm xe hay khu tiện ích để chuyển đúng nhóm.
3. **Rủi ro bỏ sót việc khẩn:** Từ khóa như “khói”, “mùi khét”, “ngập”, “người lạ đột nhập” cần được ưu tiên ngay, không chờ phân luồng thông thường.
4. **Tải công việc không đều:** Khi có sự cố diện rộng hoặc giờ cao điểm, CSKH bị tồn ticket và cư dân chờ lâu hơn.

---

## 3.2. Problem Statement (6-field)

| Field | Nội dung |
|---|---|
| **1. Actor / Operator** | Nhân viên CSKH tập trung tiếp nhận ticket; BQL từng tòa nhà; đội kỹ thuật, bảo vệ, vệ sinh và các nhà thầu xử lý. Cư dân là người khởi tạo phản ánh và nhận cập nhật. |
| **2. Current Workflow** | Cư dân gửi mô tả, ảnh và vị trí/căn hộ qua App Vinhomes Resident. CSKH đọc ticket, tra cứu tòa nhà, xác định nhóm vấn đề và mức độ ưu tiên, sau đó chuyển thủ công vào hàng chờ của BQL hoặc đội chuyên môn. BQL tiếp nhận, phân công và phản hồi tiến độ. |
| **3. Bottleneck** | Các bước 2–4 của quy trình hiện tại tốn khoảng 5–8 phút/ticket. Ticket văn bản tự do hoặc thiếu địa điểm khiến nhân viên phải đọc kỹ, tra cứu và đôi khi chuyển qua nhiều nhóm trước khi tới đúng người xử lý. |
| **4. Business Impact** | Với giả định pilot ghi nhận 1.000 ticket/ngày, riêng bước phân luồng thủ công tương đương khoảng 83–133 giờ công/ngày. Định tuyến sai hoặc chậm làm kéo dài thời gian phản hồi đầu tiên, tăng ticket tồn và ảnh hưởng trải nghiệm/hài lòng của cư dân. |
| **5. Success Metric** | (a) Giảm thời gian trung vị từ khi nhận đến khi định tuyến xuống **dưới 1 phút/ticket**. (b) Đạt **≥95%** ticket được phân loại và chuyển đúng nhóm ngay lần đầu. (c) **100%** ticket có tín hiệu cháy nổ, ngập nghiêm trọng, an ninh hoặc nguy cơ sức khỏe được gắn cờ khẩn trong SLA. (d) Giảm **≥30%** tỷ lệ ticket phải chuyển lại. |
| **6. Operational Boundary** | AI chỉ được đề xuất nhãn, mức ưu tiên và nơi nhận xử lý; không được tự đóng ticket, tự cam kết SLA, suy đoán vị trí còn thiếu, trả lời tranh chấp pháp lý hoặc hạ mức độ khẩn. Ticket khẩn cấp, độ tin cậy thấp, thiếu dữ liệu hoặc liên quan phí/tranh chấp phải qua nhân sự kiểm tra. Dữ liệu gửi vào mô hình được tối thiểu hóa và phân quyền theo vai trò. |

---

## 3.3. Future-State Flow & AI Fit

### Lựa chọn AI Fit

Giải pháp phù hợp là **LLM Feature + Rule-based Router + Human-in-the-loop**, không dùng Agent tự trị.

| Thành phần | Vai trò | Lý do lựa chọn |
|---|---|---|
| **Rule engine** | Kiểm tra trường bắt buộc, ánh xạ tòa nhà–BQL–đội xử lý, nhận diện các điều kiện khẩn cấp cứng và áp dụng SLA. | Các quy tắc an toàn phải xác định được, có thể kiểm thử và không phụ thuộc vào diễn giải của mô hình. |
| **LLM** | Đọc tiếng Việt tự do; trích xuất loại sự cố, vị trí, dấu hiệu khẩn, thực thể liên quan; tóm tắt ticket và gợi ý nhãn. | Xử lý tốt ngôn ngữ không chuẩn hóa, nhiều ý và mô tả có ngữ cảnh. |
| **HITL** | CSKH/BQL duyệt ticket có độ tin cậy thấp, thiếu thông tin, nhãn nhạy cảm hoặc nguy cơ cao. | Giữ quyền quyết định cho con người ở các trường hợp có tác động lớn. |
| **Không dùng agentic loop** | Không cho AI tự mở nhiều hệ thống, tự phân công nguồn lực, tự đóng ticket hoặc tự giao tiếp kết quả cuối với cư dân. | Quy trình định tuyến có cấu trúc; autonomy tăng rủi ro nhưng không tạo thêm giá trị tương xứng trong giai đoạn pilot. |

### Quy trình tương lai

```text
┌────────────────────┐
│ 1. Cư dân gửi ticket│
│ (nội dung, ảnh,     │
│ căn hộ/khu vực)     │
└─────────┬──────────┘
          v
┌────────────────────┐
│ 2. Tiền xử lý dữ liệu│
│ - Kiểm tra định danh │
│ - Tối thiểu hóa PII  │
│ - Kiểm tra trường    │
│   bắt buộc           │
└─────────┬──────────┘
          v
┌────────────────────┐
│ 3. 🔵 LLM trích xuất│
│ category, location, │
│ priority, evidence, │
│ confidence           │
└─────────┬──────────┘
          v
┌────────────────────┐
│ 4. 🔵 Rule router   │
│ - Tòa nhà hợp lệ?   │
│ - Queue phù hợp?    │
│ - Có tín hiệu khẩn? │
└─────────┬──────────┘
          │
    ┌─────┴──────────────────────────────┐
    │                                    │
    v                                    v
┌────────────────────┐          ┌────────────────────┐
│ 5A. Độ tin cậy cao │          │ 5B. Khẩn cấp /      │
│ & không khẩn       │          │ thiếu dữ liệu /     │
│ 🟢 Tạo ticket và   │          │ độ tin cậy thấp     │
│ chuyển đúng queue  │          │ 🟡 HITL kiểm tra    │
└─────────┬──────────┘          └─────────┬──────────┘
          │                               │
          └──────────────┬────────────────┘
                         v
              ┌────────────────────┐
              │ 6. BQL/đội xử lý   │
              │ nhận ticket, cập   │
              │ nhật tiến độ       │
              └────────────────────┘
```

### Quy tắc Human-in-the-loop

| Điều kiện | Hành động của hệ thống | Người chịu trách nhiệm |
|---|---|---|
| Điểm tin cậy ≥ ngưỡng pilot, tòa nhà hợp lệ, không có tín hiệu khẩn | Tạo ticket và chuyển tới queue đã được rule engine xác nhận. | BQL/đội nhận ticket giám sát sau phân luồng. |
| Điểm tin cậy thấp, có nhiều nhãn, thiếu vị trí hoặc tòa nhà không khớp | Hiển thị đề xuất nhãn/tuyến, yêu cầu xác nhận hoặc chỉnh sửa trước khi chuyển. | CSKH/BQL trực. |
| Cháy, khói, mùi khét, chập điện, ngập nghiêm trọng, an ninh, nguy cơ sức khỏe | Đánh dấu `EMERGENCY`, gửi cảnh báo vào kênh trực khẩn và khóa việc hạ mức ưu tiên tự động. | Bảo vệ trực, kỹ thuật trực và BQL. |
| Tranh chấp phí, pháp lý, bồi thường hoặc dữ liệu nhạy cảm | Chuyển hàng chờ chuyên trách, không sinh câu trả lời kết luận. | CSKH cấp quản lý/pháp chế theo quy trình. |

### Fallback

Nếu LLM, tích hợp định danh tòa nhà hoặc rule router gặp lỗi, hệ thống sẽ:

1. Giữ nguyên ticket gốc, thời điểm nhận và các tệp đính kèm.
2. Đặt trạng thái `MANUAL_TRIAGE_REQUIRED`.
3. Đưa ticket vào hàng chờ CSKH thủ công theo SLA hiện hành.
4. Ghi log lý do fallback để đội vận hành và kỹ thuật phân tích, không làm mất hay tự đóng ticket.

---

# Phase 5 — EVALUATE

## 5.1. Checklist đánh giá độ sẵn sàng

| Hạng mục | Tiêu chí kiểm tra | Trạng thái | Bằng chứng / hành động trước pilot |
|---|---|---|---|
| **Value** | Có vấn đề vận hành rõ và KPI đo được. | ✅ Đạt | Baseline thời gian phân luồng, tỷ lệ chuyển lại và SLA phản hồi cần được trích xuất trong 2–4 tuần gần nhất. |
| **Volume & repetition** | Đủ ticket lặp lại để huấn luyện/evaluate và tạo giá trị tự động hóa. | ✅ Đạt có điều kiện | Xác minh volume theo từng cụm đô thị; pilot khi có tập dữ liệu đại diện, gồm cả ticket thường và khẩn. |
| **Data availability** | Có nội dung ticket, metadata tòa nhà/căn hộ, lịch sử chuyển tuyến và kết quả xử lý. | 🟡 Cần xác minh | Kiểm tra quyền truy cập, độ đầy đủ của metadata và chất lượng nhãn lịch sử. |
| **Routing taxonomy** | Có danh mục loại sự cố, queue xử lý, BQL phụ trách và SLA được chuẩn hóa. | 🟡 Cần chuẩn hóa | Chốt taxonomy v1 và bảng ánh xạ tòa nhà–nhóm xử lý trước khi triển khai. |
| **Safety** | Có quy tắc cứng cho cháy nổ, ngập, an ninh và luồng escalation có người trực. | ✅ Đạt về thiết kế | Diễn tập ít nhất các kịch bản cháy/khói, ngập nặng, chập điện và người lạ đột nhập. |
| **Human oversight** | Có người chịu trách nhiệm duyệt ngoại lệ và tiếp nhận cảnh báo khẩn. | 🟡 Cần xác nhận vận hành | Xác định ca trực, quyền chỉnh sửa nhãn, SLA phê duyệt và phương án khi quá tải. |
| **Privacy & security** | Dữ liệu cư dân được tối thiểu hóa, phân quyền và có log truy cập. | 🟡 Cần phê duyệt | Thực hiện privacy/security review, data-retention policy và kiểm tra nhà cung cấp mô hình trước pilot. |
| **Integration** | App/ticketing system có API hoặc cơ chế tích hợp an toàn để tạo và cập nhật ticket. | 🟡 Cần xác minh kỹ thuật | Làm proof-of-connection tại môi trường sandbox; không ghi trực tiếp vào production ở giai đoạn đầu. |
| **Quality evaluation** | Có bộ dữ liệu gán nhãn chuẩn và quy trình đo accuracy/false negative. | 🟡 Chưa đủ | Lấy mẫu, ẩn danh và gán nhãn thủ công bởi CSKH/BQL; đặc biệt đánh giá false negative cho ticket khẩn. |
| **Fallback & observability** | Có hàng chờ thủ công, log, dashboard chất lượng và cơ chế rollback. | ✅ Đạt về thiết kế | Kiểm thử lỗi mô hình, lỗi API và lỗi ánh xạ queue trước khi mở pilot. |

## 5.2. Quyết định

### **GO — Pilot có kiểm soát**

Đề xuất triển khai pilot tại **một cụm đô thị hoặc một nhóm tòa nhà đại diện**, với phạm vi ban đầu chỉ gồm các nhóm phản ánh phổ biến, rủi ro thấp đến trung bình: hỏng đèn, vệ sinh, tiếng ồn, rò rỉ nước mức thông thường và tiện ích chung.

Các điều kiện bắt buộc trước khi bắt đầu pilot:

1. Hoàn thành bảng ánh xạ **tòa nhà → BQL → đội xử lý → SLA** và taxonomy sự cố phiên bản 1.
2. Có bộ dữ liệu lịch sử đã ẩn danh để đánh giá offline; xác nhận accuracy định tuyến ≥95% trên nhóm ticket pilot trước khi tự động chuyển các ticket tin cậy cao.
3. Kết nối và diễn tập luồng `EMERGENCY` với BQL, bảo vệ và kỹ thuật trực.
4. Hoàn tất privacy/security review và phân quyền dữ liệu theo vai trò.
5. Vận hành 4–6 tuần đầu theo mô hình **AI đề xuất + người duyệt**; chỉ bật tự động chuyển cho nhóm ticket không khẩn, metadata đầy đủ và confidence cao.

### Tiêu chí qua pilot để mở rộng

| Tiêu chí | Ngưỡng đề xuất |
|---|---|
| Thời gian trung vị đến khi route | < 1 phút/ticket |
| Độ chính xác chuyển đúng ngay lần đầu | ≥95% |
| Tỷ lệ ticket phải chuyển lại | Giảm ≥30% so với baseline |
| Ticket khẩn bị bỏ sót | 0 trường hợp trong tập đánh giá và thời gian pilot |
| CSKH/BQL chấp nhận đề xuất AI | ≥80% với các ticket đủ dữ liệu |

Nếu bất kỳ tiêu chí an toàn nào không đạt, đặc biệt là việc bỏ sót ticket khẩn, hệ thống phải quay về chế độ **AI đề xuất, bắt buộc duyệt thủ công** cho đến khi khắc phục và đánh giá lại.
