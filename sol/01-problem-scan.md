# 01 — Problem Scan & Quick Assessment

> **Lab 02 — AI Product Scoping (Vin Smart Future)**  
> **Cá nhân:** [Họ và tên] — [MSSV]  
> **Candidate được chọn để Deep-Dive:** **Problem #6 — Vinhomes: Phân loại & Điều hướng phản ánh cư dân**

---

## Phase 1 — SCAN

Theo `01-worksheet.md`, tôi sử dụng 4 lenses: **Repetitive**, **Time-consuming**, **AI-upgrade**, và **Stakeholder Pain** để quét các pain point. Tôi ưu tiên bài toán có input/output rõ, có thể đo được, và không cần dùng AI phức tạp chỉ để “ngầu”.

| # | Subsidiary | Lens chính | Problem / Bottleneck |
|---|---|---|---|
| 1 | **Vinhomes** | **Repetitive** | **Phân loại & điều hướng phản ánh cư dân:** đọc complaint free-text như mất nước, hỏng đèn, ồn ào và chuyển tới đúng bộ phận/tòa nhà. |
| 2 | **Vinpearl** | **Stakeholder Pain** | **Tổng hợp & phân tích review khách sạn:** phát hiện complaint tiêu cực/khẩn cấp từ nhiều review và đưa tới Manager. |
| 3 | **VinUni** | **Repetitive** | **Tự động hóa feedback bài lab:** đọc output autograder và draft giải thích/hint cho sinh viên, không tự quyết điểm cuối. |
| 4 | **Vinpearl** | **Time-consuming** | **Hỗ trợ xử lý group-booking email:** trích xuất ngày, số lượng phòng, yêu cầu đặc biệt trước khi kiểm tra inventory. |
| 5 | **Vinhomes** | **AI-upgrade** | **Trợ lý cư dân hỗ trợ thủ tục:** tra cứu/draft hướng dẫn đăng ký thi công, thẻ xe và thủ tục thường gặp, nhưng không tự phê duyệt. |

### Vì sao không ưu tiên một số bài toán khác?

- **Vinmec:** rủi ro khi AI sai cao hơn và cần boundary/HITL nghiêm ngặt.
- **Smart dispatch/GPS:** phụ thuộc tích hợp thời gian thực và bài toán tối ưu hóa, vượt scope prototype ngắn.
- **Các bài chỉ có luật cố định:** nếu rule/state-machine đã đủ tốt thì không nên ép dùng LLM.

---

# Phase 2 — QUICK-ASSESS

## Top 3 cá nhân

1. **#6 Vinhomes — Phân loại & điều hướng phản ánh cư dân**
2. **#8 Vinpearl — Tổng hợp & phân tích review khách sạn**
3. **#12 VinUni — Tự động hóa chấm/feedback bài lab**

> **Lưu ý:** mọi thời gian và target metric bên dưới là **scoping assumption / prototype target**, chưa phải số liệu vận hành nội bộ đã được Vingroup xác nhận.

---

## QUICK PROBLEM CARD #1 — Vinhomes complaint routing

**Bài toán (1 câu):**  
Phân loại complaint free-text của cư dân và đề xuất **category + priority + target team**, đồng thời chuyển case mơ hồ/khẩn cấp sang người xử lý.

**Công ty thành viên:** Vinhomes

**Ai đang đau (Actor)?**
- Nhân viên CSKH/Ban quản lý tiếp nhận ticket.
- Bộ phận vận hành nhận ticket sau triage.
- Cư dân bị ảnh hưởng nếu ticket chậm hoặc route sai.

### Workflow thủ công hiện tại — giả định scoping

1. Ticket từ app/kênh CSKH vào hàng đợi.
2. Nhân viên đọc complaint và ngữ cảnh.
3. Nhân viên xác định category, priority, target team.
4. Chuyển ticket tới bộ phận xử lý; nếu sai thì re-route.

**Bước tốn thời gian/lỗi nhất:** bước 2–3, ước tính **~2 phút/ticket** trong kịch bản scoping.

**AI có thể hỗ trợ:** bước 2–3.

### Prototype output

`complaint_text → category + priority + target_team + summary + needs_human_review`

### Metric có số

- **Routing Accuracy ≥ 90%**
- **Critical/Emergency Recall ≥ 95%**
- **Median AI triage latency < 10 giây/ticket**
- Case safety-sensitive hoặc không đủ thông tin phải **escalate sang human review**

### Quick Architecture

**LLM Feature + deterministic safety rules + Human-in-the-loop**

Không chọn Agent vì tác vụ cốt lõi chỉ là hiểu/classify/routing recommendation, không cần AI tự lập kế hoạch và thực hiện chuỗi hành động.

---

## QUICK PROBLEM CARD #2 — Vinpearl review intelligence

**Bài toán:**  
Đọc review khách sạn, gắn issue/severity và ưu tiên complaint cần Manager chú ý.

**Actor:** Guest Experience / Customer Service / Hotel Manager.

### Workflow hiện tại

1. Review xuất hiện trên các kênh.
2. Nhân viên đọc nội dung.
3. Gắn sentiment/issue/severity.
4. Complaint đáng chú ý được tổng hợp/escalate.

**Bottleneck:** bước 2–3, giả định **~1–3 phút/review**.

**AI Step:** `review → sentiment + issue_tags + severity + summary + urgent_flag`

**Metrics mục tiêu:**
- Urgent-complaint Recall ≥ 95%
- Issue Macro-F1 ≥ 0.85
- Latency < 10 giây/review

**Architecture:** **LLM Feature**, không cần agent.

**Điểm yếu:** định nghĩa “urgent” phụ thuộc policy; review có thể multi-issue; downstream action ít trực tiếp hơn routing ticket.

---

## QUICK PROBLEM CARD #3 — VinUni lab feedback assistant

**Bài toán:**  
Dùng output autograder + code context để draft feedback/hint, không tự quyết điểm cuối.

**Actor:** TA/Instructor; stakeholder nhận feedback là sinh viên.

### Workflow hiện tại

1. Sinh viên nộp code.
2. Autograder chạy tests.
3. TA đọc lỗi/code liên quan.
4. TA giải thích lỗi và viết hint/feedback.
5. Sinh viên sửa và nộp lại.

**Bottleneck:** bước 3–4, giả định **~3–8 phút/bài** khi cần feedback thủ công.

**AI Step:** `autograder_output + code_context → error_type + explanation + hint + feedback_draft`

**Metrics mục tiêu:**
- ≥ 90% feedback không chứa claim kỹ thuật sai trên bộ test đã review
- Draft latency < 30 giây/bài
- 100% thay đổi điểm/override do TA/Instructor quyết định

**Architecture:** **LLM Feature + existing autograder + Human review**

---

# Shortlist Score

Thang 1–5; đây là **pre-score cá nhân**, không thay thế quyết định nhóm.

| Tiêu chí | Trọng số | Vinhomes routing | Vinpearl review | VinUni feedback |
|---|---:|---:|---:|---:|
| Workflow rõ | 25% | 5 | 4 | 5 |
| AI fit hợp lý | 25% | 5 | 5 | 4 |
| Dễ tạo test set | 20% | 5 | 4 | 4 |
| Boundary kiểm soát được | 15% | 4 | 4 | 4 |
| Metric/demo rõ | 15% | 5 | 4 | 4 |
| **Weighted score** | **100%** | **4.85/5** | **4.25/5** | **4.25/5** |

## Candidate cá nhân đề xuất

**Problem #6 — Vinhomes: Phân loại & Điều hướng phản ánh cư dân.**

### Lý do chọn

- Free-text tạo giá trị thực cho NLP/LLM nhưng vẫn có thể so với baseline rule-based.
- Output có cấu trúc và đo được.
- Có thể giới hạn scope thành **triage recommendation**, không trao quyền vận hành nguy hiểm cho AI.
- Có proxy datasets trong domain property-management để kiểm tra feasibility.
- Không cần agent tự chủ.

### Giả định cần kiểm chứng trước khi triển khai thực tế

1. Tỷ lệ ticket free-text phải triage thủ công hiện tại.
2. Taxonomy category/team thực tế của Vinhomes.
3. Ticket volume/ngày, thời gian triage hiện tại và tỷ lệ re-route.
4. Hệ thống hiện tại đã dùng dropdown/rule-based routing đến mức nào.
5. Policy cho emergency/safety/financial/legal complaint.

Nếu form hiện tại đã bắt buộc category chính xác và rule-based routing gần như giải quyết hết, LLM có thể **không đáng triển khai**.

---

## Nguồn dùng để scoping

- Repo Lab: `README.md`
- Repo Lab: `01-worksheet.md`
- Repo Lab: `03-inspiration-kit.md`
- Proxy dataset tham khảo: `svr99991/india-synthetic-property-maintenance-tickets`
- Proxy dataset tham khảo: `propertypilot/property-pilot-tickets`

Các proxy dataset chỉ hỗ trợ thiết kế benchmark/schema; **không được coi là dữ liệu Vinhomes**.
