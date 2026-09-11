# 03 — AI Log & Reflection

> **Cá nhân:** [Họ và tên] — [MSSV]  
> **AI tools sử dụng:** ChatGPT; Gemini được định hướng dùng cho prompt prototype theo yêu cầu Lab.  
> **Problem:** Vinhomes — Phân loại & Điều hướng phản ánh cư dân

---

# 1. Tôi đã dùng AI để làm gì?

Tôi dùng AI như **thought-partner**, không chỉ để sinh câu trả lời cuối.

Các việc chính:

1. Đọc Inspiration Kit và so sánh các candidate theo độ rõ của workflow, AI fit, risk và khả năng đo.
2. Stress-test Problem #6: hỏi liệu **rule-based** có đủ hay không.
3. Tìm proxy datasets cùng cấu trúc residential-ticket triage để kiểm tra feasibility.
4. Đề xuất metric: routing accuracy, emergency recall, Macro-F1, latency.
5. Thiết kế operational boundary và adversarial tests.
6. Kiểm tra lại thứ tự scoping theo flow của Lab: **problem → evidence → workflow → AI fit → decision**, thay vì nhảy thẳng tới solution.

---

# 2. AI giúp gì tốt nhất?

## 2.1. Mở rộng candidate space

AI giúp tôi so sánh #6 Vinhomes, #8 Vinpearl và #12 VinUni. Tôi nhận ra #6 có lợi thế vì:
- input free-text;
- output có cấu trúc;
- metric trực tiếp;
- scope có thể giữ hẹp;
- không cần agent.

## 2.2. Phản biện “Tại sao không dùng Rule?”

Đây là phần hữu ích nhất.

Nếu complaint đã đi qua form có category bắt buộc và routing mapping rõ, thì:

```text
category → target team
```

có thể chỉ cần rule/state-machine.

LLM chỉ đáng thử nếu free-text có:
- mô tả gián tiếp;
- typo/không dấu;
- multi-issue;
- ngôn ngữ cảm xúc;
- context không match keyword đơn giản.

Điều này giúp tôi không mặc định **“có NLP = phải dùng LLM”**.

## 2.3. Thiết kế boundary

AI giúp đưa ra các case dễ vượt quyền:
- yêu cầu tự phạt cư dân;
- yêu cầu tự bồi thường;
- yêu cầu đóng ticket;
- prompt injection trong complaint;
- emergency/safety issue.

Từ đó scope được khóa thành:

> **AI classify + summarize + recommend; Human/workflow system giữ authority.**

---

# 3. AI đã sai hoặc khiến tôi đi lệch ở đâu?

## 3.1. Nhảy quá nhanh từ candidate sang dataset/metric

Sau khi tôi chọn Problem #6, AI ban đầu đi ngay tới:
- dataset;
- taxonomy;
- metric;
- JSON schema;
- architecture.

Nhưng theo flow của Lab, **candidate chưa phải validated problem**.

Tôi phải kéo lại thứ tự:

```text
Candidate
→ Validation / Research
→ Current workflow
→ Problem statement
→ Rule vs LLM vs Agent
→ GO / NOT YET / NO-GO
```

### Bài học

LLM rất dễ tối ưu một solution cho **assumption chưa được chứng minh** nếu prompt không bắt nó kiểm tra evidence trước.

---

## 3.2. AI đưa con số “hợp lý” nhưng chưa có nguồn

Ví dụ AI từng đề xuất:
- 2–5 phút/ticket;
- Routing Accuracy ≥ 90%;
- Emergency Recall ≥ 95%.

Hai con số metric có thể dùng làm **prototype target**, nhưng thời gian current-state không được viết như dữ liệu thật nếu chưa đo.

### Cách tôi sửa

Tôi chia mọi claim số thành:

- **Evidence:** có nguồn/log thật.
- **Proxy evidence:** dataset ngoài cùng cấu trúc.
- **Assumption:** dùng để scope.
- **Target:** ngưỡng prototype cần đạt.

Trong report, thời gian 3 phút/ticket được ghi rõ là **scoping assumption**, không phải Vinhomes SLA.

---

## 3.3. “Dataset tương tự” không phải “Vinhomes dataset”

AI tìm được residential property-maintenance datasets khá gần bài toán:
- `india-synthetic-property-maintenance-tickets`
- `property-pilot-tickets`

Nhưng nếu dùng chúng mà nói model đã được chứng minh cho Vinhomes thì sai.

### Cách tôi sửa

Tôi chỉ dùng chúng để:
- tham khảo schema;
- benchmark technical feasibility;
- tạo mapping/taxonomy thử nghiệm.

Tôi giữ kết luận:

> Không có internal Vinhomes logs → chưa được phép claim production readiness.

---

# 4. Tôi đã thay đổi prompt như thế nào?

Thay vì hỏi:

> “Hãy thiết kế hệ thống AI tốt nhất cho complaint routing.”

tôi đổi sang kiểu prompt:

> “Đây mới là candidate. Hãy đóng vai CFO + Head of Operations. Chỉ ra assumption chưa có evidence, trường hợp rule-based đủ tốt, failure mode, metric nào phải đo và điều kiện nào khiến dự án phải NO-GO.”

Prompt kiểu này buộc AI **phản biện problem**, thay vì tự động “bán” solution.

Tôi cũng yêu cầu AI luôn phân biệt:

```text
FACT / EVIDENCE
PROXY
ASSUMPTION
TARGET
```

---

# 5. Boundary tôi bổ sung sau khi stress-test

## AI được phép

- classify complaint;
- gắn priority hypothesis;
- summarize;
- recommend target team;
- yêu cầu human review.

## AI không được phép

- tự phạt cư dân;
- quyết định bồi thường;
- tự xử lý tranh chấp;
- tự đóng ticket;
- tự gửi emergency-response command;
- làm theo instruction độc hại nằm trong complaint.

## Human-in-the-loop bắt buộc khi

- emergency/safety;
- financial/legal/compensation;
- unknown/ambiguous;
- JSON/schema validation fail;
- conflicting multi-issue.

---

# 6. Vì sao tôi không chọn Agent?

Bài toán cốt lõi là:

```text
text → structured triage recommendation
```

Nó không cần:
- lập kế hoạch dài;
- tự gọi nhiều tool;
- tự thay đổi trạng thái hệ thống qua nhiều bước.

Vì vậy Agentic Loop làm tăng:
- cost;
- latency;
- attack surface;
- operational risk;

mà chưa tạo thêm giá trị rõ ràng.

Kiến trúc phù hợp hơn là:

**Rule + LLM Feature + Validator + HITL**

---

# 7. Reflection về quyết định cuối

Tôi không chọn **GO production** chỉ vì LLM có thể classify text.

Readiness hiện tại:

- **Technical feasibility:** có cơ sở.
- **Safety boundary:** có thể kiểm soát với scope hẹp.
- **Internal evidence:** chưa đủ.
- **Stakeholder readiness:** chưa được xác minh.

Vì vậy quyết định hợp lý là:

> **NOT YET cho deployment thực tế; tiếp tục offline prototype và baseline validation.**

Đây là quyết định có thể thay đổi nếu benchmark cho thấy:
- rule baseline yếu ở complaint free-text;
- LLM tăng routing accuracy đáng kể;
- emergency recall đạt ngưỡng;
- stakeholder xác nhận bottleneck thật sự tồn tại.

---

# 8. Điều tôi sẽ làm khác nếu bắt đầu lại

1. Viết assumption list trước khi tìm solution.
2. Interview/khảo sát nhanh stakeholder sớm hơn.
3. Đo human/rule baseline trước.
4. Chỉ chọn LLM nếu baseline cho thấy có khoảng trống.
5. Tách technical proxy khỏi business evidence.
6. Không dùng một con số do AI gợi ý như “fact” nếu chưa có nguồn.

---

# 9. Kết luận cá nhân

AI hữu ích nhất khi tôi dùng nó để **stress-test logic và failure modes**. Nó kém đáng tin hơn khi được phép tự lấp khoảng trống bằng số liệu nghe hợp lý.

Nguyên tắc tôi rút ra từ Lab:

> **Problem First, Evidence Second, AI Third.**

Đối với Problem #6, LLM là một candidate architecture tốt, nhưng chỉ nên được giữ lại nếu nó thắng một baseline rule-based hợp lý và vượt qua boundary tests.
