# 01 — Problem Scan & Quick Problem Cards
**Học viên:** Dương Minh Hiếu  
**Lab:** Lab 02 — AI Product Scoping (Vin Smart Future)  
**Chủ đề trọng tâm:** Vinhomes — Vận hành Đô thị Thông minh (Smart City Operations)

---

## 🔍 Phase 1 — SCAN: Bảng quét cơ hội vận hành Vinhomes (5 bài toán thực tế)

Dùng **4 Lenses** quét qua hoạt động vận hành tại các đại đô thị Vinhomes (Ocean Park, Smart City, Grand Park...).

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|------------|------|---------------------|
| 1 | **Vinhomes** | Lặp lại | Nhân viên CSKH phải đọc từng phản ánh của cư dân gửi qua App Vinhomes Resident, tự phán đoán phân loại và soạn phiếu/email thủ công gửi đến ban quản lý từng tòa nhà (~200 phản ánh/ngày/khu đô thị). |
| 2 | **Vinhomes** | Tốn thời gian | Nhân viên hành chính soạn thảo thông báo định kỳ (lịch bảo trì thang máy, cắt nước, sự kiện khu đô thị) bằng tay và gửi riêng lẻ theo từng cụm tòa nhà — mỗi đợt mất 2–3 giờ. |
| 3 | **Vinhomes** | AI có thể tốt hơn | Cư dân hỏi các thủ tục hành chính thường gặp (đăng ký thi công nội thất, đăng ký thẻ cư dân, vé xe tháng), CSKH trả lời rập khuôn hoặc phản hồi chậm (mất 6–12 giờ), cư dân phải lên trực tiếp sảnh văn phòng BQL. |
| 4 | **Vinhomes** | Lặp lại | Kỹ thuật viên đối soát và nhập liệu chỉ số điện/nước công tơ từ ảnh chụp thực địa tại các cụm căn hộ hằng tháng — dễ nhầm lẫn số liệu và tốn hàng chục giờ công. |
| 5 | **Vinhomes** | Pain từ người khác | Cư dân phàn nàn gay gắt khi phản ánh khẩn cấp (mùi gas rò rỉ, mất nước diện rộng, kẹt thang máy) bị gộp chung vào hòm thư chờ xử lý bình thường, gây trễ nải cứu hộ và giảm chỉ số hài lòng (NPS). |

---

## 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

### 📌 Quick Problem Card #1 — Vinhomes: Phân loại & Điều hướng phản ánh cư dân *(BÀI TOÁN CHÍNH)*

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Phân loại tự động các khiếu nại/phản ánh của     │
│ cư dân (mất nước, hỏng đèn, ồn ào...) gửi qua App          │
│ Vinhomes Resident đến đúng ban quản lý từng tòa nhà.       │
│ Công ty thành viên: [x] Vinhomes                           │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│ - Nhân viên CSKH BQL: đọc & phân loại thủ công 200+        │
│   phản ánh/ngày, dễ nhầm danh mục, nhầm tòa, routing sai.  │
│ - Cư dân: chờ phản hồi và khắc phục sự cố lâu.             │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                        │
│   1. Tiếp nhận phản ánh cư dân trên App                    │
│   → 2. Đọc nội dung & hiểu ngôn ngữ tiếng Việt             │
│   → 3. Phán đoán danh mục (KT/VS/AN/HC)                    │
│   → 4. Soạn phiếu công việc/email gửi team quản lý tòa nhà │
│   → 5. Team nhận xử lý & cập nhật trạng thái lên App       │
│                                                             │
│ Bước tốn thời gian/lỗi nhất? Bước 3 & 4 (⏱ 4–5 phút/case)  │
│ AI hỗ trợ ở bước nào? Bước 2 → 4 (Auto-classify + Draft)   │
│                                                             │
│ Metric: Giảm thời gian xử lý từ 6 phút → dưới 30 giây      │
│         Tỉ lệ routing đúng team đạt ≥ 95%                  │
│                                                             │
│ Quick Architecture: [x] LLM Feature                        │
└─────────────────────────────────────────────────────────────┘
```

---

### 📌 Quick Problem Card #2 — Vinhomes: Soạn thảo thông báo vận hành khu đô thị tự động

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Nhân viên hành chính soạn thủ công thông báo     │
│ bảo trì, lịch cắt điện nước, sự kiện và gửi riêng lẻ       │
│ theo từng cụm tòa nhà qua App Resident.                    │
│ Công ty thành viên: [x] Vinhomes                           │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│ - Nhân viên hành chính BQL: mất 2–3 giờ/đợt thông báo       │
│   cho từng tòa, lặp đi lặp lại 3–4 lần/tuần.               │
│                                                             │
│ Workflow thủ công hiện tại (3 bước):                        │
│   1. Nhận thông tin kỹ thuật/kế hoạch bảo trì               │
│   → 2. Soạn thông báo riêng phù hợp từng tòa nhà           │
│   → 3. Copy-paste và gửi broadcast qua App                 │
│                                                             │
│ Bước tốn nhất? Bước 2 (⏱ 90 phút/đợt soạn thảo)            │
│ AI hỗ trợ ở đâu? Bước 2 → 3 (Auto-draft theo template tòa) │
│                                                             │
│ Metric: Giảm 90 phút → dưới 10 phút/đợt thông báo          │
│                                                             │
│ Quick Architecture: [x] Rule + LLM Feature                 │
└─────────────────────────────────────────────────────────────┘
```

---

### 📌 Quick Problem Card #3 — Vinhomes: Trợ lý cư dân ảo hỗ trợ thủ tục hành chính & dịch vụ

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Hỗ trợ cư dân tra cứu và chuẩn bị hồ sơ đăng ký   │
│ thi công nội thất, đăng ký vé gửi xe, cấp thẻ cư dân mà   │
│ không cần trực tiếp xếp hàng tại quầy lễ tân BQL.          │
│ Công ty thành viên: [x] Vinhomes                           │
│                                                             │
│ Ai đang đau (Actor)?                                        │
│ - Cư dân mới: bối rối với quy định pháp lý/thi công        │
│   phức tạp, chuẩn bị thiếu giấy tờ phải đi lại nhiều lần.   │
│ - Lễ tân BQL: mất 50% thời gian trả lời lặp đi lặp lại     │
│   các câu hỏi về hồ sơ, quy trình cấp phép.                │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Cư dân đến quầy hoặc nhắn tin hỏi thủ tục             │
│   → 2. Lễ tân giải thích danh mục giấy tờ cần nộp          │
│   → 3. Cư dân về chuẩn bị và nộp lại hồ sơ                 │
│   → 4. Nhân viên thụ lý kiểm tra và phê duyệt              │
│                                                             │
│ Bước tốn nhất? Bước 1 & 2 (⏱ 15–20 phút tư vấn/cư dân)     │
│ AI hỗ trợ ở đâu? Bước 1 → 2 (Chatbot RAG hướng dẫn 24/7)   │
│                                                             │
│ Metric: Giảm 70% số lượt cư dân phải hỏi trực tiếp tại quầy│
│         Thời gian tra cứu thủ tục < 1 phút                  │
│                                                             │
│ Quick Architecture: [x] LLM Feature (RAG Tra cứu quy định) │
└─────────────────────────────────────────────────────────────┘
```

---

> **Bài toán được chọn để Deep-Dive:** Card #1 — Vinhomes: Phân loại & Điều hướng phản ánh cư dân  
> **Lý do lựa chọn:**
> 1. **Tần suất cao & Pain point nhức nhối:** ~200+ phản ánh/ngày/khu đô thị, chiếm hơn 20 giờ nhân công CSKH/ngày.
> 2. **Metric đo lường rõ ràng:** Rút ngắn thời gian xử lý từ 6 phút xuống dưới 30 giây, nâng độ chính xác routing lên ≥ 95%.
> 3. **Tính khả thi kỹ thuật cao:** Phù hợp hoàn hảo với giải pháp LLM Feature (xử lý ngôn ngữ tự nhiên tiếng Việt có viết tắt, cảm xúc).
> 4. **Ranh giới an toàn kiểm soát được:** Cơ chế Human-in-the-loop (HITL) với tag bắt buộc `[DRAFT_ONLY]` và Emergency Override khi phát hiện rủi ro đe dọa tính mạng (rò gas, hỏa hoạn).
