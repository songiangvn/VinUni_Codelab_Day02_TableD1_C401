# 03 — AI Log & Reflection: Nhật ký Tương tác AI
**Học viên:** Dương Minh Hiếu  
**Lab:** Lab 02 — AI Product Scoping (Vin Smart Future)  
**Chủ đề:** Vinhomes — Phân loại & Điều hướng phản ánh cư dân

---

## 📝 Nhật ký sử dụng AI trong buổi Lab

### 🤖 Công cụ AI đã sử dụng
- **Google Gemini (gemini-3.6-flash)** — qua Google GenAI SDK (Python) để xây dựng prompt prototype phân loại phản ánh cư dân và kiểm thử ranh giới an toàn.
- **AI Assistant (Gemini / ChatGPT)** — để brainstorm bài toán, phản biện thẻ Quick Problem Card, và hỗ trợ thiết kế kiến trúc AI Fit.

---

## ✅ AI đã giúp được gì?

### 1. Brainstorm danh sách bài toán nhanh
Khi dùng prompt: *"Tôi là AI Engineer tại Vin Smart Future. Hãy gợi ý 5 pain point vận hành có thể tối ưu bằng AI cho mảng Vinhomes kèm ước tính tổn thất"*, AI đã trả về danh sách có tổ chức với các bài toán liên quan trực tiếp đến App Vinhomes Resident, quản lý tòa nhà, và trải nghiệm cư dân. Tiết kiệm ~15 phút thay vì nghĩ từ đầu.

### 2. Phân tích AI Fit Matrix
Khi hỏi *"So sánh giải pháp Rule-based vs LLM Feature vs Agentic Loop cho bài toán phân loại khiếu nại cư dân bằng tiếng Việt"*, AI đã chỉ ra rõ ràng:
- Rule-based chỉ đạt ~70% accuracy do cư dân viết tự do, có lỗi chính tả, viết tắt.
- LLM Feature phù hợp nhất vì hiểu ngữ cảnh tiếng Việt tự nhiên.
- Agentic Loop quá mức cần thiết cho quy trình routing cấu trúc cố định.

Điều này giúp mình đưa ra quyết định kiến trúc nhanh và có căn cứ.

### 3. Viết System Prompt cho Gemini API
AI giúp mình diễn đạt các ràng buộc (tag `[DRAFT_ONLY]`, escalation khẩn cấp khi phát hiện cháy/ngập/rò gas) thành ngôn ngữ hướng dẫn rõ ràng cho LLM. Đặc biệt, AI gợi ý mình dùng structured output format (phân loại + routing + JSON action) thay vì free-form text — giúp kiểm soát ranh giới tốt hơn.

---

## ❌ AI đã sai / Hallucination ở đâu?

### 1. Số liệu thống kê bịa
Khi hỏi về số lượng phản ánh cư dân trung bình tại Vinhomes, AI trả lời: *"Vinhomes nhận trung bình 500 phản ánh/ngày/khu đô thị"*. Nhưng khi hỏi nguồn, AI thừa nhận đây là ước tính giả định, không có dữ liệu thực.

**→ Cách sửa:** Tôi điều chỉnh xuống con số bảo thủ hơn (~200 phản ánh/ngày) và ghi rõ đây là ước tính, cần xác minh với BQL Vinhomes thực tế.

### 2. Đề xuất dùng Multi-Agent System không cần thiết
Lần đầu hỏi về kiến trúc, AI đề xuất: *"Xây dựng hệ thống 3 Agent: Agent phân loại, Agent routing, Agent follow-up"*. Đây là over-engineering — quy trình classify → route → confirm hoàn toàn có thể giải quyết bằng 1 LLM call duy nhất.

**→ Cách sửa:** Prompt lại: *"Ưu tiên giải pháp đơn giản nhất. 1 LLM call có đủ không?"*. AI chuyển sang đề xuất LLM Feature đơn giản — đúng hướng.

### 3. Bỏ qua ranh giới khi bị "cầu xin"
Khi chạy adversarial test với prompt yêu cầu bỏ tag `[DRAFT_ONLY]`, lần đầu (chưa có system prompt cứng) model sẵn sàng tuân theo. Điều này chứng minh ranh giới phải được lập trình nghiêm ngặt.

**→ Cách sửa:** Viết lại System Prompt với ngôn ngữ tuyệt đối: *"EVERY response starts with [DRAFT_ONLY]. Never omit it."* Và yêu cầu model trả lời theo structured format cố định. Sau khi sửa, model giữ vững ranh giới qua mọi adversarial test.

---

## 💡 Bài học rút ra

1. **AI là công cụ hỗ trợ tư duy, không phải nguồn sự thật.** Số liệu thống kê và metric phải được cross-check với dữ liệu thực tế của doanh nghiệp.

2. **Structured output > Free-form text khi cần kiểm soát ranh giới.** Yêu cầu model trả lời theo format cố định giúp phát hiện vi phạm ranh giới dễ hơn và giảm thiểu rủi ro.

3. **Adversarial testing trước khi deploy là bắt buộc.** Không thể tin ranh giới an toàn chỉ vì nó hoạt động đúng với input bình thường — phải chủ động tấn công thử.

4. **Giải pháp đơn giản luôn tốt hơn.** Một LLM Feature với HITL có thể giải quyết hầu hết bài toán phân loại text mà không cần hệ thống Multi-Agent phức tạp.
