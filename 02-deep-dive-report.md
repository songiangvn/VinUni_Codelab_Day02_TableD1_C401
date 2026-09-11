# 02 — Deep Dive Report: Vinhomes Phân loại & Điều hướng Phản ánh Cư dân
**Học viên:** Dương Minh Hiếu  
**Lab:** Lab 02 — AI Product Scoping (Vin Smart Future)  
**Bài toán được chọn:** Card #1 — Vinhomes / Phân loại & Điều hướng phản ánh cư dân

---

## 🏗️ Phase 3 — DEEP DIVE

### 3.1. Current-State Workflow Mapping

Quy trình xử lý phản ánh cư dân hiện tại tại Ban Quản Lý (BQL) Vinhomes:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │     │ Bước 2       │     │ Bước 3       │     │ Bước 4       │
│ Cư dân gửi   │     │ NV CSKH đọc  │     │ NV phán đoán │     │ Soạn email & │
│ phản ánh qua │ ──→ │ từng phản ánh│ ──→ │ danh mục     │ ──→ │ gửi phiếu    │
│ App Resident │     │ trên hệ thống│     │ (KT/VS/AN?)  │     │ đến team     │
│              │     │              │     │              │     │ tương ứng    │
│ Ai: Cư dân   │     │ Ai: NV CSKH  │     │ Ai: NV CSKH  │     │ Ai: NV CSKH  │
│ ⏱ —          │     │ ⏱ 1 phút     │     │ ⏱ 2 phút 🔴  │     │ ⏱ 3 phút 🔴  │
│ In: Mô tả VN │     │ In: App data │     │ In: Nội dung │     │ In: Danh mục │
│ Out: Ticket   │     │ Out: Hiểu ý  │     │ Out: Tag phân │     │ Out: Email    │
│              │     │              │     │ loại         │     │ routing      │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                      │
                                                                      ▼
                                                               ┌──────────────┐
                                                               │ Bước 5       │
                                                               │ Team nhận,   │
                                                               │ xử lý & cập  │
                                                               │ nhật trạng   │
                                                               │ thái lên App │
                                                               │ 🔄 Handoff   │
                                                               │ ⏱ Tùy case   │
                                                               └──────────────┘
🔴 = Bottlenecks (Bước 2 & 3: phán đoán + soạn email thủ công)
🔄 = Handoff (Bước 4 → 5: CSKH → Team kỹ thuật/vệ sinh/an ninh)
⏱ Tổng thời gian xử lý thủ công: ~6 phút/phản ánh × 200 phản ánh/ngày = 20 giờ nhân công/ngày
```

---

### 3.2. Problem Statement (6-field)

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Nhân viên CSKH (Customer Service) tại Ban Quản Lý Vinhomes từng khu đô thị (Ocean Park, Grand Park, Smart City...). |
| **2. Current Workflow** | Khi cư dân gửi phản ánh qua App Vinhomes Resident, NV CSKH phải: (1) đọc nội dung bằng tiếng Việt, (2) tự phán đoán phản ánh thuộc danh mục gì (kỹ thuật/vệ sinh/an ninh/hành chính), (3) mở email soạn phiếu công việc gửi đến đúng team quản lý tòa nhà tương ứng, (4) cập nhật trạng thái lên App. Toàn bộ thủ công, mất ~6 phút/case, ~200 case/ngày. |
| **3. Bottleneck** | Bước 2 & 3 (mất ~5 phút): NV phải đọc hiểu ngôn ngữ tự nhiên (tiếng Việt, có lỗi chính tả, viết tắt, cảm xúc mạnh), tự phán đoán danh mục và soạn phiếu routing. Tỉ lệ phân loại sai hiện ~12%, dẫn đến phản ánh bị gửi nhầm team, kéo dài thời gian xử lý thêm 24–48 giờ. |
| **4. Business Impact** | ~200 phản ánh/ngày/khu đô thị × 6 phút = 20 giờ nhân công CSKH/ngày. Tỉ lệ routing sai 12% gây delay xử lý, khiến NPS cư dân giảm và cư dân gọi tổng đài escalate. Chi phí nhân sự CSKH chuyên đọc và phân loại phản ánh ước tính ~150 triệu VND/tháng/khu đô thị. |
| **5. Success Metric** | 1. Giảm thời gian phân loại + routing từ 6 phút → dưới 30 giây/phản ánh (Efficiency: giảm 95%). 2. Tỉ lệ phân loại đúng danh mục ≥ 95% (Quality — hiện 88%). 3. Giảm SLA phản hồi cư dân từ 12 giờ → dưới 2 giờ (Customer Satisfaction). |
| **6. Operational Boundary** | **AI được phép:** Đọc nội dung phản ánh, phân loại danh mục, soạn phiếu routing dạng DRAFT có nhãn `[DRAFT_ONLY]`. **TUYỆT ĐỐI CẤM:** (1) AI không được tự gửi phiếu đi khi chưa có NV CSKH phê duyệt (HITL bắt buộc). (2) Nếu phản ánh liên quan đến an toàn tính mạng (cháy, ngập, rò gas, sập kết cấu — rủi ro thương tích > 5%), AI phải kích hoạt team khẩn cấp ngay, KHÔNG route về bảo trì thông thường. (3) AI không được tự xử lý tranh chấp pháp lý hoặc tài chính — phải chuyển cho quản lý cấp cao. |

---

### 3.3. Future-State Flow & AI Fit

**AI Fit:** Chọn **LLM Feature** — sử dụng LLM để hiểu ngôn ngữ tự nhiên tiếng Việt (có viết tắt, lỗi chính tả, cảm xúc) và phân loại + draft routing. Không cần Agent tự trị vì quy trình có cấu trúc cố định và rủi ro khi routing sai phản ánh khẩn cấp có thể ảnh hưởng đến an toàn cư dân.

**Quy trình tương lai (Future-State):**

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │     │ Bước 2       │     │ Bước 3       │     │ Bước 4       │
│ Cư dân gửi   │     │ 🔵 AI auto-  │     │ 🔵 AI draft  │     │ 🟢 NV CSKH   │
│ phản ánh qua │ ──→ │ classify:    │ ──→ │ phiếu routing│ ──→ │ review & 1-  │
│ App Resident │     │ KT/VS/AN/HC  │     │ [DRAFT_ONLY] │     │ click duyệt  │
│              │     │ + priority   │     │ → đúng team  │     │ → gửi team   │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
⏱ —                  ⏱ <5 giây            ⏱ <5 giây            ⏱ 15 giây
                                                                      │
                                                               ↩️ Fallback:
                                                               Nếu AI confidence
                                                               < 80% hoặc trả lỗi,
                                                               NV CSKH phân loại
                                                               thủ công như cũ.
                                                               ──────────────────
                                                               🚨 Khẩn cấp:
                                                               Nếu AI phát hiện
                                                               cháy/ngập/gas →
                                                               dispatch_emergency_team
                                                               ngay lập tức.
```

**Ký hiệu:**
- 🔵 **AI Step:** Tác vụ được LLM xử lý tự động.
- 🟢 **Human Step (HITL):** NV CSKH duyệt và nhấn gửi — bắt buộc.
- ↩️ **Fallback:** Khi AI confidence thấp hoặc lỗi → xử lý thủ công.
- 🚨 **Emergency Override:** Phản ánh nguy hiểm tính mạng → escalate ngay.

**AI-Fit Matrix:**
| Giải pháp | Lý do chọn/loại bỏ |
|---|---|
| **Rule / State-Machine** | Không đủ linh hoạt: cư dân viết tự do bằng tiếng Việt, có lỗi chính tả, viết tắt, cảm xúc. Rule-based keyword matching chỉ đạt ~70% accuracy. |
| **✅ LLM Feature** | Phù hợp nhất: LLM hiểu ngữ cảnh tiếng Việt tự nhiên, phân loại chính xác, soạn phiếu routing tự động. Kiểm soát qua HITL + emergency override. |
| **Agentic Loop** | Quá mức cần thiết: quy trình routing có cấu trúc cố định (classify → route → confirm), không cần agent tự trị ra quyết định phức tạp. |

---

## 🏁 Phase 5 — EVALUATE

### AI Readiness Checklist:

1. ✅ Chúng tôi có sẵn dữ liệu mẫu/logs sạch để test?  
   → Vinhomes có database phản ánh cư dân từ App Resident (hàng trăm nghìn records có sẵn danh mục đã được gắn thủ công → dùng làm training/eval data).
2. ✅ Rủi ro khi AI sai có nằm trong tầm kiểm soát (qua HITL hoặc Fallback)?  
   → Có. NV CSKH bắt buộc duyệt trước khi gửi. Emergency override tự động escalate khi phát hiện nguy hiểm. Fallback về workflow cũ nếu AI không tự tin.
3. ✅ Stakeholders sẵn sàng thay đổi quy trình làm việc cũ?  
   → Có. NV CSKH phàn nàn nhiều về tình trạng đọc phản ánh lặp đi lặp lại, sẵn sàng adopt tool hỗ trợ phân loại tự động.

### Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future:

**[x] GO — Bắt đầu xây dựng Prototype với scope hẹp.**

**Justification (Lý giải quyết định dựa trên bằng chứng kỹ thuật và chi phí):**

> Bài toán đáp ứng đủ 3 điều kiện GO:
> 1. **Bài toán cụ thể, tần suất cao:** ~200 phản ánh/ngày/khu đô thị, 6 phút/case → 20 giờ nhân công/ngày. Metric rõ ràng (30 giây, 95% accuracy, SLA < 2 giờ).
> 2. **Giải pháp kỹ thuật feasible:** LLM Feature đã chứng minh phân loại text tiếng Việt chính xác tại nhiều doanh nghiệp lớn. Dữ liệu training có sẵn từ App Resident. Chi phí API Gemini rất thấp (~$0.001/phản ánh).
> 3. **Rủi ro kiểm soát được:** HITL bắt buộc, emergency override cho phản ánh nguy hiểm, fallback khi AI không tự tin. Ranh giới an toàn `[DRAFT_ONLY]` được lập trình cứng.
>
> **Scope prototype đề xuất:** Triển khai thử nghiệm tại 1 khu đô thị Vinhomes Ocean Park trong 4 tuần. Đo: thời gian xử lý/phản ánh, tỉ lệ phân loại đúng, NPS cư dân trước/sau.
