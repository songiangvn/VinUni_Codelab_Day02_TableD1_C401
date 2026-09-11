# 02 — Deep-Dive Report
### Dự án: **Resident Triage Copilot** — Phân loại & Điều hướng phản ánh cư dân Vinhomes
**Đơn vị thực hiện:** Vin Smart Future × Khối Vận hành Vinhomes
**Phạm vi pilot:** 01 phân khu chung cư (giả định ~24 tòa / ~12.000 căn hộ đã bàn giao)

---

## 📇 Tóm tắt một trang (Executive Summary)

| | |
|---|---|
| **Vấn đề** | Mọi phản ánh của cư dân gửi qua App Vinhomes Resident đều phải đi qua một nút thắt duy nhất: một nhân viên CSKH của BQL đọc tay mô tả tiếng Việt tự do, tự đoán phiếu thuộc tổ nào, tự gán mức khẩn. Nút thắt này không co giãn được theo giờ cao điểm. |
| **Giải pháp** | Một **service phân loại** đứng giữa App và hệ thống vận hành: chuẩn hoá → phân loại (nhóm/tiểu nhóm/độ ưu tiên/tổ tiếp nhận) → trả về kèm `confidence` và `margin` → auto-route khi chắc chắn, đẩy sang người khi không chắc. Kèm draft tin phản hồi gắn thẻ `[DRAFT_ONLY]`. |
| **Kiến trúc** | **Hybrid: Rule guard + LLM Feature.** Không dùng Agentic Loop. |
| **Ranh giới cốt lõi** | AI **không bao giờ** tự gửi tin cho cư dân; AI **không có quyền hạ cấp** một phiếu khẩn cấp; AI **không** cam kết phí/pháp lý; AI **không** tiết lộ thông tin cư dân khác. |
| **Quyết định** | ✅ **GO — nhưng theo cổng (staged).** Bật ở chế độ *shadow* trước; chỉ mở auto-route khi gold set chứng minh **0 phiếu P0 bị hạ nhãn**. |

---

# 🏗️ Phase 3 — DEEP-DIVE

## 3.1. Current-State Workflow Mapping

> 🖼️ Bản vẽ đầy đủ (Current-State + Future-State, có đánh dấu Handoff / Bottleneck / thời gian): xem **[04-workflow-diagram.png](04-workflow-diagram.png)**.

### Sơ đồ quy trình hiện tại

```text
  👤 CƯ DÂN                                    🏢 BAN QUẢN LÝ TÒA NHÀ
 ─────────────                              ──────────────────────────────

┌──────────────┐
│ Bước 1       │
│ Gõ phản ánh  │
│ + ảnh trên   │
│ App Resident │
│ Ai: Cư dân   │
│ ⏱ 2 phút     │
│ Out: Text tự │
│      do +ảnh │
└──────┬───────┘
       │  🔄 HANDOFF #1  (App ──> hàng đợi chung của BQL)
       ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 2  🔴   │     │ Bước 3  🔴   │     │ Bước 4  🔴   │     │ Bước 5       │
│ Phiếu NẰM    │     │ CSKH đọc mô  │     │ CSKH tự đoán │     │ Tổ chuyên    │
│ CHỜ trong    │ ──▶ │ tả; gọi lại  │ ──▶ │ tổ + tự gán  │ ──▶ │ môn nhận     │
│ hàng đợi     │     │ xác minh nếu │     │ ưu tiên; nhập│     │ phiếu, đi    │
│ chung        │     │ thiếu tin    │     │ hệ thống     │     │ hiện trường  │
│ Ai: —        │     │ Ai: CSKH     │     │ Ai: CSKH     │     │ Ai: Tổ KT/VS │
│ ⏱ TB 25 phút │     │ ⏱ 4 phút     │     │ ⏱ 2 phút     │     │ ⏱ 30–240 ph  │
│   cao điểm   │     │ (~30% phải   │     │ ❗sai tổ ~12% │     │              │
│   45ph–3 giờ │     │  gọi lại)    │     │              │     │              │
└──────────────┘     └──────────────┘     └──────┬───────┘     └──────┬───────┘
                                                 │                    │
                              🔄 HANDOFF #2 ─────┘                    │
                              (CSKH ──> Tổ chuyên môn)                │
                                                                      │
        ┌─────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────┐                                   ┌──────────────┐
│ Bước 5b 🔴   │  Nếu SAI TỔ (~12% phiếu)          │ Bước 6  🔴   │
│ Tổ đẩy ngược │ ─────────────────────────────┐    │ CSKH gõ tay  │
│ về CSKH      │  🔄 HANDOFF #3 (vòng ngược)  │    │ tin phản hồi │
│ ⏱ +6 GIỜ trễ │                              │    │ đóng phiếu   │
│ + làm lại B4 │ ◀────────────────────────────┘    │ Ai: CSKH     │
└──────────────┘                                   │ ⏱ 5 phút     │
                                                   │ (copy-paste  │
                                                   │  template)   │
                                                   └──────┬───────┘
                                                          │
                                                  🔄 HANDOFF #4
                                                  (BQL ──> App ──> Cư dân)
                                                          ▼
                                                   ┌──────────────┐
                                                   │ Cư dân nhận  │
                                                   │ tin đóng     │
                                                   │ phiếu        │
                                                   └──────────────┘

🔴 = Bottleneck    🔄 = Handoff
```

### Bảng chi tiết từng bước

| Bước | Ai làm | Công cụ | Thời gian **công** | Thời gian **chờ** | Ghi chú |
|---|---|---|---:|---:|---|
| 1. Cư dân gửi phản ánh | Cư dân | App Vinhomes Resident | 2 ph | — | Mô tả tự do, thường thiếu tòa/căn, ảnh mờ |
| 2. Nằm trong hàng đợi | — | Hàng đợi chung BQL | 0 | **25 ph TB / 45 ph–3 giờ cao điểm** 🔴 | Không có phân luồng theo mức khẩn |
| 3. CSKH đọc & xác minh | CSKH | Đọc tay + gọi điện | **4 ph** 🔴 | — | ~30% phiếu phải gọi lại cư dân |
| 4. Đoán tổ + gán ưu tiên | CSKH | Phần mềm vận hành | **2 ph** 🔴 | — | Cảm tính, phụ thuộc kinh nghiệm ca trực |
| 5. Tổ chuyên môn xử lý | Tổ KT/VS/AN | Hiện trường | 30–240 ph | — | Ngoài phạm vi dự án |
| 5b. Đẩy ngược nếu sai tổ | Tổ → CSKH | Phần mềm | +2 ph | **+6 giờ** 🔴 | Xảy ra với ~12% phiếu |
| 6. Soạn tin phản hồi | CSKH | Template + gõ tay | **5 ph** 🔴 | — | Rập khuôn → cư dân thấy "cho có" |

> **⏱ Tổng thời gian CÔNG của BQL cho phần triage + phản hồi: ~11 phút/phiếu**
> **⏱ Tổng LEAD TIME cư dân cảm nhận (gửi → nhận phản hồi): trung bình ~12 giờ** — con số này khớp với mô tả bài toán #6 trong Inspiration Kit của Lab (*"CSKH phản hồi rập khuôn, mất 12 tiếng"*).

### 🔎 Ba bottleneck thật sự — và điều quan trọng nhất về chúng

1. **Bước 2 (hàng đợi) là bottleneck lớn nhất, nhưng KHÔNG phải bottleneck về kỹ năng.** Nó là bottleneck về **năng lực tiếp nhận**: số phiếu đến vào 18h–21h vượt số người trực. Đây là chỗ AI có giá trị *cấu trúc*, vì máy co giãn được còn ca trực thì không.
2. **Bước 3–4 là bottleneck về nhận thức.** CSKH phải dịch từ "ngôn ngữ cư dân" sang "ngôn ngữ vận hành". Người mới vào ca làm chậm và sai nhiều hơn người cũ — chất lượng triage phụ thuộc vào **ai đang trực**, đó là một lỗi thiết kế quy trình chứ không phải lỗi của nhân viên.
3. **Bước 5b (vòng đẩy ngược) là bottleneck đắt nhất tính trên mỗi lần xảy ra.** Một phiếu đi sai tổ không chỉ mất thêm 2 phút công — nó mất **cả nửa ngày** vì phải chờ ca sau, và cư dân thường đã nhắc lại lần 2 trước khi phiếu được xử lý.

> 💡 **Quan sát quyết định thiết kế:** ba bottleneck trên đều nằm **trước** lúc tổ kỹ thuật ra hiện trường. Nghĩa là dự án này **không cố làm thợ sửa nhanh hơn** — nó chỉ cố đưa đúng phiếu đến đúng thợ, sớm hơn. Phạm vi hẹp đó chính là lý do dự án khả thi.

---

## 3.2. Problem Statement (6-field) & Metrics

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | **Nhân viên CSKH / Trực ban của Ban Quản lý tòa nhà Vinhomes** — người tiếp nhận và phân luồng 100% phiếu phản ánh trong ca. Người chịu ảnh hưởng gián tiếp: **cư dân** (người chờ) và **các tổ nghiệp vụ** (Điện, Nước, Cơ điện, Thang máy, Vệ sinh, An ninh, Cảnh quan, Hành chính). |
| **2. Current Workflow** | Cư dân gửi phản ánh dạng **văn bản tiếng Việt tự do + ảnh** qua App Vinhomes Resident. Phiếu rơi vào **một hàng đợi chung không phân luồng**. CSKH đọc tay từng phiếu, gọi lại xác minh khi mô tả thiếu thông tin (~30% **[E]**), **tự phán đoán** phiếu thuộc tổ nào và **tự gán** mức ưu tiên bằng cảm tính, nhập vào phần mềm vận hành rồi chuyển tổ chuyên môn. Sau khi tổ xử lý xong, CSKH **gõ tay tin phản hồi** (thực chất là chọn template cứng) để đóng phiếu. Toàn bộ 6 bước là thủ công, tốn **~11 phút công/phiếu**, lead time cư dân cảm nhận **~12 giờ**. |
| **3. Bottleneck** | **Bước 2–4 — khâu triage.** Cụ thể: (a) phiếu nằm chờ trung bình 25 phút, giờ cao điểm 18h–21h lên tới 45 phút–3 giờ vì số phiếu đến vượt năng lực ca trực; (b) việc **đọc hiểu mô tả tiếng Việt tự do** (không dấu, sai chính tả, mô tả gián tiếp, một phiếu chứa nhiều vấn đề) và **quyết định tổ + mức ưu tiên** hoàn toàn dựa vào kinh nghiệm cá nhân → **~12% phiếu bị route sai [E]**, mỗi lần sai tốn thêm ~6 giờ trễ. Đây là khâu xử lý ngôn ngữ tự nhiên nặng nhất trong toàn luồng. |
| **4. Business Impact** | Trên phạm vi 1 phân khu (~12.000 căn hộ **[E]**, ~4.200 phiếu/tháng ≈ **140 phiếu/ngày [E]**):<br>• **~25,7 giờ công/ngày** (≈ 3,2 FTE) chỉ để triage + soạn phản hồi.<br>• **~17 phiếu/ngày đi sai tổ**, mỗi phiếu trễ thêm ~6 giờ → vừa tốn công vừa sinh phiếu nhắc lại.<br>• Giờ cao điểm buổi tối là lúc cư dân bức xúc nhất **lại là lúc hàng đợi dài nhất** → rủi ro trực tiếp lên **điểm hài lòng cư dân và uy tín thương hiệu Vinhomes**.<br>• **Rủi ro đuôi (tail risk):** một phiếu khẩn cấp (mùi gas, kẹt thang máy, ngập) nằm lẫn trong hàng đợi 3 giờ là một sự cố an toàn, không phải một sự cố dịch vụ. Đây là tổn thất không quy ra tiền được. |
| **5. Success Metric** | **Ngưỡng chấp nhận của sản phẩm (đo trên gold set 500 phiếu đã gán nhãn thủ công):**<br>**M1 — Chất lượng:** Top-1 routing accuracy **≥ 92%**; **macro-F1 ≥ 0,85** (bắt buộc dùng macro vì các lớp cực mất cân bằng — nếu chỉ đo accuracy, model đoán bừa lớp phổ biến vẫn đẹp số).<br>**M2 — Độ phủ tự động:** **≥ 75%** phiếu đủ điều kiện auto-route (`confidence ≥ 0,80` **và** `margin ≥ 0,05`).<br>**M3 — Tốc độ:** Time-to-assign **P90 ≤ 60 giây** (baseline: TB 25 phút, P90 giờ cao điểm ~45 phút).<br>**M4 — Sai sót:** tỉ lệ route sai **từ ~12% → ≤ 5%**.<br>**M5 — Hiệu suất người:** thời gian công triage + phản hồi **từ 11 phút → ≤ 4 phút/phiếu**.<br>**M6 — 🚨 METRIC CHẶN GO-LIVE (hard gate):** **0 phiếu P0 (khẩn cấp) bị hạ nhãn xuống non-P0** trên gold set. Không có ngưỡng "chấp nhận được" nào khác. Nếu M6 không đạt, dù M1–M5 đẹp đến đâu, **không mở auto-route**. |
| **6. Operational Boundary** | **✅ AI ĐƯỢC PHÉP:**<br>1. Đọc nội dung phiếu, chuẩn hoá văn bản (thêm dấu, sửa chính tả), trích xuất tòa/căn/tầng.<br>2. Đề xuất `category`, `subcategory`, `priority` (P0–P3), `route_to`, kèm `confidence` và `margin`.<br>3. Tự động chuyển phiếu tới tổ nghiệp vụ **chỉ khi** `confidence ≥ 0,80` **và** `margin ≥ 0,05` **và** không thuộc lớp khẩn cấp.<br>4. Soạn **bản nháp** tin phản hồi cư dân, **bắt buộc** mở đầu bằng thẻ `[DRAFT_ONLY]`.<br><br>**🚫 AI TUYỆT ĐỐI KHÔNG ĐƯỢC:**<br>1. **Tự gửi bất kỳ tin nào tới cư dân.** Mọi tin phải qua nút duyệt của CSKH. Thẻ `[DRAFT_ONLY]` là khoá chặn — hệ thống gửi tin sẽ từ chối mọi payload còn chứa thẻ này, và từ chối mọi payload *không đi qua* đường duyệt.<br>2. **Hạ cấp một phiếu khẩn cấp.** Nếu lớp rule khẩn cấp (cháy, khói, mùi gas, kẹt thang máy, ngập, điện giật, cấp cứu y tế) đã bật cờ, LLM **không có quyền** gán P1/P2/P3 cho phiếu đó. Cờ chỉ được gỡ bởi con người.<br>3. **Cam kết về phí, hoàn tiền, miễn phí quản lý, trách nhiệm pháp lý hay bồi thường** — kể cả khi cư dân hoặc nhân viên yêu cầu trực tiếp.<br>4. **Tiết lộ thông tin cá nhân của cư dân khác** (tên, SĐT, số căn, lịch sử phiếu) — tuân thủ **Nghị định 13/2023/NĐ-CP** về bảo vệ dữ liệu cá nhân.<br>5. **Hứa mốc thời gian xử lý cụ thể** nếu mốc đó không đến từ bảng SLA đã cấu hình sẵn.<br>6. **Nhận chỉ thị từ nội dung phiếu.** Văn bản cư dân gửi là **dữ liệu**, không phải **mệnh lệnh** (chống prompt injection).<br><br>**🟢 ĐIỂM BẮT BUỘC CÓ NGƯỜI DUYỆT (HITL):** (i) mọi tin gửi ra cho cư dân; (ii) mọi phiếu có `confidence < 0,80` hoặc `margin < 0,05`; (iii) mọi phiếu chạm ranh giới cấm ở trên.<br>**🔺 NGOẠI LỆ CỦA HITL:** phiếu **P0 khẩn cấp** được đẩy **ngay** lên Trung tâm điều hành + hotline 24/7 **mà không chờ duyệt** — vì với lớp này, *chậm* nguy hiểm hơn *thừa*. Đây là ngoại lệ có chủ đích, không phải lỗ hổng. |

---

### 📊 Bảng phân loại (Taxonomy) — 9 nhóm × tổ tiếp nhận × SLA

Đây là "bảng chân lý" mà model phải bám vào. Nhãn không được tự do sinh; model chỉ được chọn trong danh sách đóng này.

| Mã | Nhóm phản ánh | Ví dụ tiểu nhóm | Tổ tiếp nhận | Ưu tiên mặc định | SLA phản hồi đầu |
|---|---|---|---|:---:|---|
| `SC-KHAN` | **Sự cố khẩn cấp** | Cháy/khói, mùi gas, kẹt thang máy, ngập, điện giật, y tế | Trung tâm điều hành + Hotline 24/7 | **P0** | **Ngay lập tức (≤ 2 phút)** |
| `KT-DIEN` | Kỹ thuật – Điện | Mất điện căn hộ, hỏng đèn hành lang, aptomat nhảy | Tổ Kỹ thuật Điện | P2 | 4 giờ |
| `KT-NUOC` | Kỹ thuật – Cấp thoát nước | Mất nước, nước yếu, rò rỉ, tắc cống, thấm trần | Tổ Kỹ thuật Nước | P1–P2 | 2–4 giờ |
| `KT-CODIEN` | Kỹ thuật – Cơ điện/ĐHKK | Điều hòa, thông gió, hút mùi, máy bơm | Tổ Cơ điện | P2 | 8 giờ |
| `KT-THANGMAY` | Kỹ thuật – Thang máy | Thang rung/ồn, dừng tầng sai, cửa chậm *(kẹt người → `SC-KHAN`)* | Tổ Thang máy + nhà thầu | P1 | 2 giờ |
| `VS-MT` | Vệ sinh & Môi trường | Rác không thu, mùi hôi khu rác, hành lang bẩn, côn trùng | Tổ Vệ sinh | P3 | 12 giờ |
| `AN-NINH` | An ninh & Trật tự | Ồn ào, karaoke, đỗ xe sai, người lạ, vật nuôi | Tổ An ninh | P2 | 4 giờ |
| `CQ-XANH` | Cảnh quan & Cây xanh | Cây đổ/nghiêng, đèn sân vườn, sân chơi hỏng | Tổ Cảnh quan | P3 | 24 giờ |
| `DV-HC` | Dịch vụ & Hành chính | Phí quản lý, thẻ cư dân, đăng ký thi công, vé gửi xe | Tổ CSKH / Hành chính | P3 | 24 giờ |

**Thang ưu tiên:** `P0` = nguy hiểm tính mạng/tài sản, xử lý ngay · `P1` = ảnh hưởng nhiều căn hoặc mất tiện ích thiết yếu · `P2` = ảnh hưởng 1 căn hộ · `P3` = phiền toái/hành chính.

---

### 💰 Mô hình kinh tế — và điều mà mô hình này KHÔNG nói

| Khoản mục | Hiện tại | Sau khi có AI (mục tiêu) | Cách tính |
|---|---:|---:|---|
| Khối lượng phiếu | 140/ngày | 140/ngày | 12.000 căn × 0,35 phiếu/căn/tháng ÷ 30 **[E]** |
| Thời gian công/phiếu | 11 phút | ≤ 4 phút | M5 |
| Giờ công/ngày | ~25,7 h | ~9,3 h | 140 × phút ÷ 60 |
| **Tiết kiệm (trần lý thuyết)** | — | **~16,4 giờ công/ngày** | Hiệu số |
| **Tiết kiệm (đã chiết khấu 40% ma sát thực tế)** | — | **~10 giờ công/ngày ≈ 1,2 FTE** | Nhóm cố ý hạ kỳ vọng |
| Chi phí inference LLM | — | **~$5–16/tháng** | 4.200 phiếu × ~1.550 token; giá Gemini 2.5 Flash **[E — cần verify bảng giá tại thời điểm triển khai]** |

> ### ⚠️ Điểm trung thực quan trọng nhất của phần tài chính này
> **Token không phải là chi phí của dự án này.** Vài chục đô một tháng là nhiễu. Chi phí thật là:
> - **1 AI Engineer × 8 tuần + 0,5 Backend Engineer × 4 tuần** (one-off),
> - **2 người × 3 ngày gán nhãn** gold set 500 phiếu (one-off, và phải làm lại định kỳ),
> - **Chi phí vận hành liên tục:** giám sát drift, đánh giá lại hằng tuần, cập nhật taxonomy khi BQL đổi cơ cấu tổ.
>
> Một dự án AI chết vì khoản thứ ba, không phải khoản đầu. Nhóm ghi rõ ở đây để không tự lừa mình bằng con số "$5/tháng".
>
> **Lý do kinh tế thật sự để làm:** chi phí biên khi nhân rộng gần bằng 0. Làm xong cho 1 phân khu thì phân khu thứ 2, thứ 20 gần như chỉ tốn công cấu hình taxonomy. Đó mới là luận điểm đầu tư, không phải 10 giờ công/ngày của một phân khu.

---

## 3.3. Future-State Flow & AI Fit

### 🎯 AI-Fit Matrix — so sánh ba lựa chọn

| | **Rule / State-Machine** | **LLM Feature** ✅ | **Agentic Loop** |
|---|---|---|---|
| **Cách làm** | Bảng từ khoá → tổ | Model đọc hiểu mô tả, trả JSON có cấu trúc | Agent tự lập kế hoạch, tự gọi tool, tự tạo work order, tự nhắn cư dân |
| **Ăn được gì** | Phiếu viết chuẩn, đúng từ khoá | Tiếng Việt tự do, không dấu, sai chính tả, mô tả gián tiếp, phiếu đa vấn đề | Về lý thuyết: cả quy trình |
| **Sập ở đâu** | *"trần nhà vệ sinh ố vàng nhỏ giọt"* (không có chữ "nước"); *"mat nuoc tu sang"*; teencode | Phiếu quá mơ hồ, phiếu bịa, ảnh là thông tin chính | Không kiểm soát được hành động; khó audit; lỗi lan theo chuỗi |
| **Độ chính xác** | **80% đúng + 20% chuyển người an toàn, 0% route sai** — *đo thật* trên bộ 30 phiếu hạt giống (xem phụ lục). ⚠️ n=30 quá nhỏ để kết luận; **[M]** phải đo lại trên gold set 500 phiếu | Mục tiêu ≥ 92% (M1) | Không đo được ổn định cho bài này |
| **Biết lúc nào mình sai?** | ❌ Không. Rule luôn "tự tin". | ✅ Có — `confidence` + `margin` cho phép hệ thống tự nhường cho người | ⚠️ Có nhưng lỗi tích luỹ qua nhiều bước |
| **Rủi ro** | Thấp | **Trung bình, chặn được bằng HITL + rule guard** | **Cao — không tương xứng lợi ích** |
| **Kết luận** | Giữ lại làm **lớp chặn khẩn cấp + fallback**, không dùng làm bộ phân loại chính | **CHỌN** | **Loại** |

### ✅ Quyết định: **Hybrid — Rule Guard + LLM Feature**

Ba lý do:

1. **Giá trị thật nằm ở việc hiểu tiếng Việt tự do**, và đó đúng là việc LLM làm tốt nhất — nhưng đó là *một bước phân loại*, không phải một quy trình cần lập kế hoạch. Dùng Agent ở đây là dùng búa tạ đóng đinh mũ.
2. **Quy trình vận hành BQL đã có cấu trúc cố định.** Tổ nào làm gì, SLA bao nhiêu — tất cả đã được quy định. Không có gì để agent "tự nghĩ ra". Cái cần là *ánh xạ đúng*, không phải *sáng tạo*.
3. **Rủi ro bất đối xứng.** Agent tự tạo work order hoặc tự nhắn cư dân là loại lỗi mà BQL không thể rút lại. LLM Feature giữ mọi hành động ra bên ngoài nằm sau một nút bấm của con người.

> **Lớp Rule vẫn ở lại, nhưng đổi vai.** Nó không còn là bộ phân loại chính — nó trở thành **lớp chặn khẩn cấp chạy TRƯỚC LLM** (regex/từ khoá: cháy, khói, gas, kẹt thang, ngập, điện giật, cấp cứu) và **lưới an toàn khi LLM sập**. Đây là kiến trúc *defense-in-depth*: ranh giới quan trọng nhất không được phép chỉ sống trong prompt.

---

### 🔄 Sơ đồ Future-State Flow

```text
┌──────────────┐
│ Bước 1       │  👤 Cư dân gửi phản ánh trên App
│ + App gợi ý  │     (App bổ sung: tự điền tòa/căn từ profile,
│   tòa/căn tự │      dropdown danh mục thô — làm TRƯỚC khi có AI)
│   động       │
│ ⏱ 2 phút     │
└──────┬───────┘
       ▼
╔══════════════════════════════════════════════════════════════════╗
║           🛡️  LỚP 0 — RULE GUARD  (chạy trước LLM, ~5ms)         ║
║   Regex/từ khoá khẩn cấp: cháy · khói · mùi gas · kẹt thang máy  ║
║   · ngập · điện giật · cấp cứu                                   ║
╚═════════════╤════════════════════════════════════╤═══════════════╝
              │ KHỚP                               │ KHÔNG KHỚP
              ▼                                    ▼
   ┌────────────────────────┐        ┌────────────────────────────┐
   │ 🚨 P0 — ĐẨY NGAY       │        │ Bước 2  🔵 AI TRIAGE       │
   │ Trung tâm điều hành    │        │ Chuẩn hoá text → phân loại │
   │ + Hotline 24/7         │        │ category / subcategory /   │
   │ + Cảnh báo BQL tòa     │        │ priority / route_to        │
   │                        │        │ + confidence + margin      │
   │ ⚠️ LLM KHÔNG có quyền  │        │ ⏱ ~2 giây                  │
   │    hạ cấp phiếu này    │        └──────────┬─────────────────┘
   │ ⏱ ≤ 2 giây             │                   │
   └────────────────────────┘                   ▼
                                    ╔═══════════════════════════╗
                                    ║  Bước 3 — CỔNG QUYẾT ĐỊNH ║
                                    ║  confidence ≥ 0,80  AND   ║
                                    ║  margin     ≥ 0,05  ?     ║
                                    ╚═══╤═══════════════════╤═══╝
                                    ĐẠT │                   │ KHÔNG ĐẠT
                                        ▼                   ▼
                        ┌───────────────────────┐  ┌──────────────────────┐
                        │ Bước 4a  🔵 AUTO-ROUTE│  │ Bước 4b 🟢 HUMAN     │
                        │ Phiếu vào thẳng hàng  │  │ Vào hàng review của  │
                        │ đợi của tổ chuyên môn │  │ CSKH — AI gợi ý      │
                        │ đúng, đúng mức ưu tiên│  │ TOP-3 nhãn kèm lý do │
                        │ ⏱ ≤ 60 giây (P90)     │  │ ⏱ ~1 phút            │
                        │ Mục tiêu: ≥75% phiếu  │  │ (~25% phiếu)         │
                        └───────────┬───────────┘  └──────────┬───────────┘
                                    └──────────┬──────────────┘
                                               ▼
                                    ┌────────────────────────┐
                                    │ Bước 5 — Tổ chuyên môn │
                                    │ xử lý hiện trường      │
                                    └───────────┬────────────┘
                                                ▼
                                    ┌────────────────────────┐
                                    │ Bước 6  🔵 AI DRAFT    │
                                    │ tin phản hồi cư dân    │
                                    │ BẮT BUỘC mở đầu bằng   │
                                    │ [DRAFT_ONLY]           │
                                    └───────────┬────────────┘
                                                ▼
                                    ┌────────────────────────┐
                                    │ Bước 7  🟢 CSKH DUYỆT  │
                                    │ Đọc → sửa nếu cần →    │
                                    │ bấm GỬI                │
                                    │ ⚠️ Cổng gửi TỪ CHỐI    │
                                    │   payload còn chứa     │
                                    │   thẻ [DRAFT_ONLY]     │
                                    └───────────┬────────────┘
                                                ▼
                                    ┌────────────────────────┐
                                    │ 👤 Cư dân nhận phản hồi│
                                    └────────────────────────┘

              ┌───────────────────────────────────────────────┐
              │  🔁 VÒNG HỌC (chạy nền)                       │
              │  Mỗi lần CSKH SỬA nhãn của AI → ghi vào       │
              │  label store → đánh giá lại hằng tuần →       │
              │  cập nhật prompt/taxonomy. Người sửa máy      │
              │  là dữ liệu, không phải là thất bại.          │
              └───────────────────────────────────────────────┘

🔵 = AI Step   🟢 = Human-in-the-loop   🚨 = Đường khẩn cấp   ↩️ = Fallback (xem dưới)
```

### ↩️ Thang Fallback — 4 nấc, không nấc nào làm mất phiếu

| Nấc | Tình huống | Hành vi hệ thống |
|:---:|---|---|
| **F1** | LLM trả JSON sai định dạng / thiếu trường | Retry 1 lần với nhiệt độ 0 và lời nhắc schema. |
| **F2** | Vẫn lỗi, **hoặc** LLM timeout > 5 giây | Rớt xuống **rule-based keyword router v0**. Phiếu vẫn được gán tổ (kém chính xác hơn), gắn cờ `fallback_rule`. |
| **F3** | Rule cũng không khớp gì | Phiếu vào **hàng đợi chung của CSKH đúng như quy trình hiện tại**. Hệ thống thoái lui về trạng thái cũ — không tệ hơn hôm nay. |
| **F4** | Service AI sập hoàn toàn / vượt quota | **Bypass toàn cục.** 100% phiếu đi thẳng hàng đợi chung. Có cảnh báo cho đội vận hành. Cư dân không bao giờ nhận ra có sự cố. |

> **Nguyên tắc bất biến:** *Không có nấc fallback nào được phép làm rơi một phiếu, hay im lặng không phản hồi cư dân.* Trạng thái xấu nhất của hệ thống mới **đúng bằng** trạng thái bình thường của hệ thống cũ.

---

### 🛡️ Cách ranh giới được thi hành (không chỉ nằm trong prompt)

Đây là phần nhóm đầu tư nhiều nhất, vì bài học lớn nhất khi stress-test là: **một ranh giới chỉ nằm trong system prompt là một ranh giới có thể bị nói cho biến mất.**

| Lớp | Cơ chế | Chặn được gì |
|:---:|---|---|
| **L1** | System prompt nghiêm ngặt + structured output (JSON schema đóng) | Phần lớn yêu cầu vượt rào thông thường |
| **L2** | **Deterministic post-validator trong code** — kiểm tra sau khi LLM trả lời: có thẻ `[DRAFT_ONLY]`? nhãn có nằm trong taxonomy đóng? cờ khẩn cấp có bị hạ không? có chứa PII/cam kết phí không? | **Mọi trường hợp L1 bị thuyết phục.** Nếu L2 phát hiện vi phạm → ghi đè kết quả, ép về `escalate_human_review`, ghi log sự cố |
| **L3** | **Cổng gửi tin (message gateway)** từ chối mọi payload còn chứa `[DRAFT_ONLY]`, và từ chối mọi payload không mang chữ ký phê duyệt của CSKH | AI **về mặt kiến trúc** không có đường gửi tin cho cư dân, kể cả khi L1 và L2 đều bị qua mặt |

> L1 là *lời khuyên*. L2 là *luật*. L3 là *khoá vật lý*. Chỉ có L3 mới thực sự khiến ranh giới trở thành không thể vi phạm — và nhóm học được điều này chính từ bài test prompt injection TC2 (xem [03-ai-log.md](03-ai-log.md)).

### 📉 Kết quả đo thật trên bộ 30 phiếu hạt giống

Nhóm tự gán nhãn 30 phiếu tiếng Việt (có cài 7 phiếu bẫy: gõ không dấu, đa vấn đề, mồi lấy PII, mồi cam kết phí, kẹt-thang-máy-nhưng-không-có-người) và chạy lớp rule qua để lấy baseline. **Lần chạy đầu tìm ra hai bug thật:**

| | Lần 1 | Sau khi sửa |
|---|---:|---:|
| Đúng hoàn toàn | 23/30 (77%) | **24/30 (80%)** |
| Chuyển người (an toàn) | 5/30 (17%) | 6/30 (20%) |
| **Route sai tổ** | **2/30 (7%)** | **0/30 (0%)** |
| **🚨 P0 bị bỏ sót (M6)** | **1** | **0** |

**Bug 1 —** mẫu `chay nha` khớp vào giữa chuỗi `chay nhap nhay` ("đèn chạy nhấp nháy" gõ không dấu) → một cái đèn nhấp nháy bị báo động **cháy nhà**. Sửa: bắt buộc `\b` ở hai đầu mọi mẫu bỏ dấu.

**Bug 2 —** phiếu *"thang máy đang kẹt, có 2 người bị nhốt bên trong"* bị auto-route xuống Tổ Thang máy như phiếu bảo trì thường, SLA 2 giờ. Mẫu cũ đòi hai chữ `ket thang may` đứng cạnh nhau. Sửa: đổi định nghĩa khẩn cấp từ *"thang máy hỏng"* sang **"có người bị kẹt"** (`bị nhốt`, `mắc kẹt`, `kẹt trong thang`) — tín hiệu thật là **con người**, không phải cái thang.

> ⚠️ n = 30 quá nhỏ để kết luận về độ chính xác. Giá trị của phép đo này không nằm ở con số 80% — mà ở chỗ **nó tìm ra hai lỗi mà việc đọc code không tìm ra**, trong đó một lỗi đúng là loại mà metric M6 sinh ra để chặn. Đây chính là lý do giai đoạn P0 (gán nhãn) được đặt trước mọi thứ khác trong kế hoạch triển khai.

---

# 🏁 Phase 5 — EVALUATE

## AI Readiness Checklist

### 1. Chúng tôi có sẵn dữ liệu mẫu/logs sạch để test? — ⚠️ **CHƯA / Một phần**

Vinhomes **có** lịch sử phiếu phản ánh trong hệ thống vận hành, nhưng nhóm **chưa có bộ nhãn chuẩn (gold set)** — và đây là khoảng trống lớn nhất của dự án. Không có gold set thì mọi con số ở mục Success Metric chỉ là nguyện vọng.

**Việc phải làm ngay, không đàm phán:**
- Trích **500 phiếu lịch sử** (lấy mẫu phân tầng theo tổ và theo khung giờ, **cố ý lấy dư phiếu khẩn cấp** vì lớp này hiếm nhưng quan trọng nhất).
- **2 người gán nhãn độc lập × 3 ngày**, đo **inter-annotator agreement (Cohen's κ)**. Nếu **κ < 0,7** thì vấn đề không nằm ở model — mà là **chính con người cũng không thống nhất được taxonomy**, và phải sửa taxonomy trước khi viết một dòng prompt nào.
- Ẩn danh dữ liệu theo **Nghị định 13/2023/NĐ-CP** trước khi đưa ra khỏi hệ thống.

### 2. Rủi ro khi AI sai có nằm trong tầm kiểm soát? — ✅ **CÓ**

| Loại lỗi | Hậu quả | Cơ chế chặn | Đánh giá |
|---|---|---|:---:|
| Route sai tổ (P2/P3) | Trễ vài giờ, đúng bằng mức tệ hôm nay | Vòng học + human review khi `margin` thấp | ✅ Chấp nhận được |
| AI tự gửi tin cho cư dân | Nghiêm trọng — mất kiểm soát truyền thông | `[DRAFT_ONLY]` + L2 validator + **L3 message gateway** | ✅ Chặn ở tầng kiến trúc |
| **Hạ cấp phiếu khẩn cấp** | **Nguy hiểm tính mạng** | **Rule guard chạy trước LLM; LLM không có quyền gỡ cờ; metric M6 chặn go-live** | ✅ Chặn, nhưng **phải kiểm chứng bằng gold set** |
| Lộ thông tin cư dân khác | Vi phạm NĐ 13/2023 | Boundary + L2 validator quét PII | ✅ Chặn |
| Cam kết phí/pháp lý | Tranh chấp với cư dân | Boundary + HITL bắt buộc | ✅ Chặn |
| Prompt injection từ nội dung phiếu | Vượt mọi ranh giới L1 | L2 + L3 (kiến trúc, không phụ thuộc prompt) | ✅ Chặn |

### 3. Stakeholders sẵn sàng thay đổi quy trình? — ⚠️ **CẦN XÁC NHẬN [M]**

Đây là rủi ro bị đánh giá thấp nhất trong mọi dự án AI nội bộ. Cụ thể với dự án này: **nếu CSKH nghĩ công cụ này để thay thế họ, họ sẽ không sửa nhãn sai — và vòng học chết ngay từ tuần đầu.** Dữ liệu tốt nhất của dự án đến từ chính những lần con người sửa máy.

Nhóm đề xuất ba việc: (a) định vị sản phẩm rõ ràng là **copilot, không phải autopilot** — CSKH vẫn là người ra quyết định cuối; (b) ghi nhận và **thưởng** cho việc sửa nhãn, coi đó là đóng góp chuyên môn; (c) chạy **shadow mode 2 tuần** để CSKH nhìn thấy AI đoán gì trước khi AI được phép làm gì.

---

## 🧭 Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future

> # ✅ **GO — theo cổng (Staged GO)**

**Không phải "GO" trọn gói, và cũng không phải "NOT YET".** Nhóm chọn một quyết định có cấu trúc:

| Giai đoạn | Nội dung | Điều kiện mở cổng sang giai đoạn sau |
|:---:|---|---|
| **P0 — Gán nhãn**<br>(Tuần 1–2) | Trích 500 phiếu, 2 người gán nhãn độc lập, đo κ, chốt taxonomy | **κ ≥ 0,7.** Nếu không đạt → **dừng, sửa taxonomy**, đây là điểm rút lui rẻ nhất của dự án |
| **P1 — Shadow mode**<br>(Tuần 3–4) | AI chạy song song, **chỉ ghi log, không route gì cả**. Đo M1/M6 trên dữ liệu thật | **M1 ≥ 92%** và **M6 = 0 phiếu P0 bị hạ nhãn** |
| **P2 — Auto-route hẹp**<br>(Tuần 5–6) | Chỉ mở auto-route cho **3 nhóm an toàn nhất** (`VS-MT`, `CQ-XANH`, `DV-HC` — toàn P3, sai cũng không nguy hiểm). Mọi nhóm khác vẫn qua người | Không có sự cố; CSKH chấp nhận |
| **P3 — Mở rộng + Draft reply**<br>(Tuần 7–8) | Mở dần các nhóm kỹ thuật; bật tính năng draft tin phản hồi (Card #2) | Đạt M2 ≥ 75%, M4 ≤ 5% |
| **P4 — Nhân rộng** | Sang phân khu thứ 2, thứ 3 | Chi phí biên thấp — đây mới là lúc dự án sinh lời thật |

### Justification — lý giải dựa trên bằng chứng

**Vì sao GO chứ không phải NO-GO:**
Bài toán nằm đúng vào vùng LLM vượt trội rõ rệt so với rule (hiểu tiếng Việt tự do, không dấu, mô tả gián tiếp, phiếu đa vấn đề). Nhóm đã tự phản biện bằng vai CFO và không bác bỏ được luận điểm này — rule-based *đã* được cân nhắc nghiêm túc, và nó vẫn ở lại trong kiến trúc, chỉ là ở đúng vai của nó (lớp chặn + fallback), không phải vai bộ phân loại chính. Về rủi ro: mọi hành động ra bên ngoài đều nằm sau nút bấm của con người, và ranh giới quan trọng nhất được thi hành ở tầng kiến trúc (L3) chứ không phải tầng prompt. Về chi phí: chi phí thử sai thấp, và fallback đảm bảo trạng thái xấu nhất chỉ bằng hiện trạng.

**Vì sao không phải "GO" trọn gói:**
Vì điều kiện tiên quyết số 1 — **dữ liệu có nhãn — chưa tồn tại.** Bật auto-route trước khi có gold set là quyết định dựa trên niềm tin chứ không phải bằng chứng, và với một lớp phiếu có rủi ro tính mạng thì đó là điều không thể chấp nhận. Ngoài ra, rủi ro ở đây **bất đối xứng**: một phiếu vệ sinh route sai tốn vài giờ, một phiếu mùi gas route sai là một sự cố an toàn. Một quyết định "GO" phẳng sẽ đối xử với hai loại rủi ro đó như nhau — nên nhóm chia cổng và mở đúng theo thứ tự rủi ro tăng dần.

**Điểm rút lui (kill criteria) — nhóm cam kết trước:**
- Nếu **κ < 0,7** sau P0 → dừng, không phải lỗi model mà là lỗi định nghĩa bài toán.
- Nếu **M6 ≠ 0** sau P1 (dù chỉ **một** phiếu P0 bị hạ nhãn) → **không mở auto-route**, quay lại thiết kế rule guard.
- Nếu sau P2 tỉ lệ CSKH sửa nhãn > 40% → công cụ đang tạo việc chứ không giảm việc → dừng và thiết kế lại.

> 🎯 **Nguyên tắc xuyên suốt của nhóm:** *Chúng tôi không tối ưu để AI được dùng nhiều nhất. Chúng tôi tối ưu để AI được dùng ở đúng chỗ nó đáng tin — và bị chặn ở chỗ nó không đáng tin.*

---

## 📎 Phụ lục

- **[04-workflow-diagram.png](04-workflow-diagram.png)** — Sơ đồ Current-State & Future-State
- **[starter-code/prompt_prototype.py](starter-code/prompt_prototype.py)** — Prompt prototype + 5 adversarial test cases
- **[extras/taxonomy.md](extras/taxonomy.md)** — Bảng taxonomy đầy đủ, dạng máy đọc được
- **[extras/gold-set-sample.jsonl](extras/gold-set-sample.jsonl)** — 30 phiếu mẫu tiếng Việt đã gán nhãn (hạt giống cho gold set 500 phiếu)
- **[03-ai-log.md](03-ai-log.md)** — Nhật ký làm việc với AI: AI giúp gì, sai gì, nhóm sửa gì
