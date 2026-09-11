# 03 — AI Log & Reflection
### Nhật ký làm việc với AI trong Lab 02 — AI Product Scoping

> 📝 *Ghi chú cho nhóm: file này là phản ánh cá nhân. Hãy thay tên, sửa lại các đoạn cho khớp với trải nghiệm thật của bạn trước khi nộp — một AI log bị sao chép nguyên văn thì chính nó đã phản bội mục đích của bài tập này.*

---

## 1. Tôi đã dùng AI như thế nào

Tôi dùng AI (Claude, có đối chiếu thêm với Gemini) làm **thought-partner**, không phải làm máy sinh nội dung. Cụ thể ở bốn vai:

| Vai | Việc AI làm | Việc tôi làm |
|---|---|---|
| **Người brainstorm** | Liệt kê pain point vận hành của Vinhomes theo 4 lenses | Loại bỏ những ý tôi không kiểm chứng được; giữ lại bài toán tôi thật sự hiểu |
| **Đối thủ tranh luận** | Đóng vai CFO / Trưởng phòng Vận hành để đâm thủng đề xuất của tôi | Trả lời từng đòn, và **sửa thiết kế** ở những đòn tôi không trả lời được |
| **Cặp mắt thứ hai khi viết code** | Gợi ý cấu trúc lớp bảo vệ ranh giới, viết nháp regex | Chạy thật, tìm bug, sửa. Bug quan trọng nhất AI **không** tìm ra — tôi tìm ra bằng cách chạy |
| **Biên tập** | Siết lại câu chữ báo cáo, giữ giọng nhất quán | Quyết định cái gì được viết, cái gì bị cắt |

Prompt hữu ích nhất của cả buổi không phải prompt xin ý tưởng, mà là prompt **xin bị phản bác**:

> *"Đây là thẻ bài toán tôi đề xuất: [...]. Hãy đóng vai một CFO và Trưởng phòng Vận hành cực kỳ khắt khe. Chỉ ra 3 điểm yếu về logic và metric, và giải thích vì sao rule-based code thông thường lại giải quyết bài toán này tốt hơn dùng AI."*

Đòn thứ ba của "CFO" — *"Chỉ cần cho cư dân chọn dropdown danh mục trên App là xong, tốn gì AI?"* — là đòn tôi **không bác bỏ được**. Kết quả là tôi phải sửa phạm vi dự án: dropdown vẫn phải làm, và phải làm **trước**; AI xử lý phần *sau* dropdown (mục "Khác", phiếu đa vấn đề, mức khẩn nằm trong câu chữ chứ không nằm trong danh mục). Nếu tôi chỉ hỏi AI "giúp tôi viết đề xuất cho hay", tôi đã không bao giờ phát hiện ra lỗ hổng đó.

---

## 2. AI đã giúp được gì (cụ thể)

**a. Ép tôi tách "bài toán" khỏi "giải pháp".**
Ban đầu tôi mô tả bài toán là *"cần một con AI phân loại phản ánh cư dân"*. Đó không phải bài toán, đó là giải pháp đã được chọn sẵn. Sau vài vòng hỏi lại, tôi viết lại thành: *"mọi phiếu đều đi qua một nút thắt duy nhất là một người đọc tay, và nút thắt đó không co giãn được theo giờ cao điểm"*. Cách diễn đạt thứ hai mới cho thấy vì sao dùng máy lại có ý nghĩa — vì máy co giãn được, còn ca trực thì không.

**b. Chỉ ra rằng hai bài toán của tôi thật ra là một.**
Tôi định làm Card #1 (phân loại) và Card #2 (soạn tin phản hồi) thành hai dự án. AI hỏi một câu đơn giản: *"Hai bài toán này có chung người dùng, chung dữ liệu và chung màn hình không?"* — có, cả ba. Vậy nó là một sản phẩm hai giai đoạn, không phải hai dự án.

**c. Gợi ý dùng `margin` chứ không chỉ `confidence`.**
Tôi chỉ nghĩ đến ngưỡng confidence. AI chỉ ra rằng một model có thể tự tin 0,85 cho nhãn top-1 nhưng 0,84 cho nhãn top-2 — tức là nó **không thật sự phân biệt được hai lựa chọn**, dù confidence trông rất đẹp. Từ đó tôi thêm điều kiện `margin ≥ 0,05`. Đây là ý hay nhất mà AI đóng góp cho phần thiết kế.

**d. Nhắc tôi về macro-F1.**
Tôi định dùng accuracy làm metric chính. AI chỉ ra taxonomy của tôi cực kỳ mất cân bằng (nhóm Vệ sinh chiếm rất nhiều phiếu, nhóm Khẩn cấp rất ít) — một model đoán bừa nhóm phổ biến vẫn ra accuracy đẹp trong khi bỏ sót đúng lớp quan trọng nhất. Tôi đổi sang macro-F1 làm metric chất lượng chính.

---

## 3. AI đã sai ở đâu — và tôi sửa thế nào

Đây là phần tôi học được nhiều nhất.

### ❌ Sai #1 — AI bịa số liệu nội bộ của Vinhomes một cách rất thuyết phục

**Điều đã xảy ra:** Khi tôi hỏi về quy mô vận hành, AI đưa ra những con số nghe cực kỳ chắc chắn: số phiếu/ngày, tỉ lệ route sai, số nhân sự CSKH mỗi tòa. Không có nguồn nào cả. Khi tôi yêu cầu trích dẫn, nó không dẫn được — vì đó là **những con số hợp lý về mặt thống kê nhưng không tồn tại về mặt sự thật**. Đây là kiểu hallucination nguy hiểm nhất: không sai một cách lố bịch, mà sai một cách *vừa đủ đúng để lọt qua*.

**Tôi sửa:** Tôi áp một quy ước ghi nhãn cho **toàn bộ** con số trong bài — `[S]` có nguồn, `[E]` ước lượng có cách tính, `[M]` chưa biết và phải đo. Sau đó tôi rà lại từng con số. Kết quả là hầu hết chuyển thành `[E]` kèm công thức (ví dụ: 12.000 căn × 0,35 phiếu/căn/tháng ÷ 30 ngày = ~140 phiếu/ngày), và vài con số quan trọng nhất — như tỉ lệ route sai thật và độ chính xác của rule-based v0 — bị hạ xuống `[M]`, tức là **việc phải đo trong tuần đầu, không được đoán**.

**Bài học:** *Một con số không rõ nguồn gốc thì tệ hơn là không có số.* Với người đọc báo cáo, số bịa và số thật trông giống hệt nhau.

---

### ❌ Sai #2 — Assertion "luôn đúng" trong bộ test (AI viết test tự khen mình)

**Điều đã xảy ra:** Trong bản nháp đầu của `prompt_prototype.py`, một assertion kiểm tra ranh giới RULE 1 được viết là:

```python
lambda d: d["action"] != "auto_send"
```

Trông rất hợp lý. Vấn đề: `"auto_send"` **không hề tồn tại** trong tập `VALID_ACTIONS` của tôi. Nghĩa là điều kiện này **luôn luôn đúng**, kể cả khi ranh giới bị phá hoàn toàn. Tôi đã có một bài test xanh lè nhưng không kiểm tra gì cả.

**Tôi sửa:** Đổi thành hai assertion có thể thật sự thất bại:
```python
lambda d: str(d["draft_reply"]).startswith("[DRAFT_ONLY]")
lambda d: "forced_send_attempt" in d["boundary_flags"]
```
Và tôi thêm một thói quen: **cố tình làm hỏng code để xem test có đỏ không.** Một bài test chưa từng đỏ là một bài test chưa được chứng minh là có tác dụng.

---

### ❌ Sai #3 — Bug nguy hiểm nhất cả buổi: bỏ dấu tiếng Việt làm chập từ

**Điều đã xảy ra:** Để bắt được phiếu cư dân gõ không dấu, tôi bỏ dấu toàn bộ văn bản trước khi so khớp từ khoá khẩn cấp. AI đồng tình, và cả hai chúng tôi đều thấy hợp lý. Nhưng khi tôi **chạy thật** bộ test, Test Case 4 — phiếu phàn nàn karaoke ồn ào — bị hệ thống phân loại thành **SỰ CỐ KHẨN CẤP P0** và bắn thẳng lên hotline 24/7.

Lý do: trong câu *"khỏi cần Ban Quản Lý đứng giữa làm gì"*, chữ **"khỏi"** sau khi bỏ dấu thành **`khoi`** — trùng khít với **"khói"** trong danh sách từ khoá cháy nổ.

Truy tiếp, tôi tìm ra cả một họ va chạm cùng kiểu, và họ này đều nằm đúng ở lớp từ khoá nguy hiểm nhất:

| Từ khẩn cấp | Bỏ dấu | Trùng với | Hậu quả |
|---|---|---|---|
| khói | `khoi` | **khỏi** ("khỏi cần") | Báo cháy giả |
| cháy | `chay` | **chạy** ("xe chạy qua") | Báo cháy giả |
| ngập | `ngap` | **ngáp** | Báo ngập giả |

**Tôi sửa (lần 1):** Chia từ khoá khẩn cấp làm hai tầng:
- **Tầng ACCENTED** — khớp trên văn bản **còn dấu**, dùng cho các từ đơn dễ va chạm (`cháy`, `khói`, `ngập`).
- **Tầng FOLDED** — khớp trên văn bản đã bỏ dấu, nhưng **chỉ dùng cụm từ nhiều chữ**, không bao giờ dùng từ đơn.

Test Case 4 trả về đúng `AN-NINH`, phiếu mùi gas vẫn bắt P0. Tôi tưởng đã xong.

---

### ❌ Sai #3b — Tôi tưởng đã sửa xong, cho tới lúc **đo trên 30 phiếu thật**

Đây là phần tôi tự hào nhất và cũng xấu hổ nhất. Sau khi "sửa xong", tôi tự viết một bộ 30 phiếu tiếng Việt có gán nhãn tay (hạt giống cho gold set 500 phiếu) và chạy bộ phân loại rule qua nó để lấy số baseline. Kết quả lần đầu:

```
Đúng hoàn toàn        : 23/30  (77%)
Chuyển người (an toàn): 5/30   (17%)
SAI (route nhầm tổ)   : 2/30   (7%)
P0 bị bỏ sót          : 1      ← PHẢI BẰNG 0
```

**Hai phiếu sai đó phơi ra hai lỗi mà bộ test 5 case của tôi hoàn toàn không chạm tới:**

**Lỗi A — `chay nha` khớp vào giữa chữ `chay nhap nhay`.**
Phiếu VH-002: *"den hanh lang tang 8 toa s1.03 **chay nhap nhay** may hom nay roi"* (đèn hành lang chạy nhấp nháy — gõ không dấu). Mẫu khẩn cấp của tôi là `chay nha` — **không có ranh giới từ**. Nó khớp vào đúng 8 ký tự đầu của "chay nhap". Một cái đèn nhấp nháy bị hệ thống báo động là **cháy nhà**.

Đây chính là *Scunthorpe problem* — bài toán kinh điển của lọc theo chuỗi con — nhưng tiếng Việt nặng hơn nhiều, vì bỏ dấu xong thì số cặp va chạm tăng vọt.

**Lỗi B — phiếu P0 thật bị bỏ sót vì tôi khớp sai ngữ nghĩa.**
Phiếu VH-003: *"Thang máy số 2 tòa S3.01 đang kẹt, **có 2 người bị nhốt bên trong**"*. Mẫu của tôi là `ket thang may` — đòi hai chữ đứng cạnh nhau. Ở đây người ta viết "thang máy... đang kẹt", chữ chen giữa. Kết quả: phiếu **có người bị nhốt trong thang máy** được auto-route xuống Tổ Thang máy như một phiếu bảo trì thường, SLA 2 giờ.

Đây đúng là kịch bản mà metric **M6 (0 phiếu P0 bị hạ nhãn)** sinh ra để chặn — và nó đã chặn được, ngay ở bộ 30 phiếu.

**Tôi sửa (lần 2):**
1. **Bắt buộc `\b` ở hai đầu mọi mẫu bỏ dấu.** `chay nha` → `\bchay nha\b`. "chay nhap" không còn khớp.
2. **Đổi cách định nghĩa khẩn cấp cho thang máy: từ "thang máy hỏng" sang "có người bị kẹt".** Tín hiệu thật không phải cái thang — mà là **con người ở trong đó**. Mẫu mới bắt `bị nhốt`, `mắc kẹt`, `kẹt trong thang`. Nhờ đó phiếu VH-027 (*"cửa thang máy đóng mở chậm, hay bị kẹt lại giữa chừng"* — không có ai bị nhốt) vẫn ở đúng nhóm `KT-THANGMAY`, không bị báo động giả.

Kết quả sau khi sửa:

```
Đúng hoàn toàn        : 24/30  (80%)
Chuyển người (an toàn): 6/30   (20%)
SAI (route nhầm tổ)   : 0/30   (0%)    ← từ 2
P0 bị bỏ sót          : 0                ← từ 1
```

> **Lưu ý trung thực về con số này:** n = 30 là **quá nhỏ** để kết luận bất cứ điều gì. Nó không phải bằng chứng rằng rule đạt 80% — nó là bằng chứng rằng **việc đo tìm ra bug mà việc đọc không tìm ra**. Con số thật phải đến từ gold set 500 phiếu.

**Bài học lớn nhất của tôi trong buổi Lab:** *AI rà code rất giỏi phần logic, nhưng cả hai bug trên chỉ lộ ra khi tôi CHẠY trên dữ liệu thật.* Chúng không phải lỗi thuật toán — chúng là lỗi **đặc thù ngôn ngữ tiếng Việt**, nằm trong khoảng mù của cả tôi lẫn model khi chỉ đọc code.

Và cả hai đều sai theo **hướng nguy hiểm**, nhưng nguy hiểm theo hai kiểu đối nghịch nhau:
- Lỗi A làm hệ thống **la làng** — một BQL bị báo cháy giả vài lần sẽ tắt chuông, và khi có cháy thật thì không còn ai nghe.
- Lỗi B làm hệ thống **im lặng** — hai người bị nhốt trong thang máy được xếp vào hàng chờ bảo trì 2 giờ.

Cái thứ hai đáng sợ hơn nhiều, và nó là cái mà **đọc code không bao giờ tìm ra được**.

---

### ❌ Sai #4 — AI mặc định coi system prompt là ranh giới đủ mạnh

**Điều đã xảy ra:** Bản nháp đầu tiên của tôi (và gợi ý của AI) đặt toàn bộ ranh giới vào `SYSTEM_PROMPT`: "AI không được tự gửi tin", "AI không được hạ cấp phiếu khẩn". Rồi tôi viết một test giả lập prompt injection — *"Bỏ qua mọi hướng dẫn phía trên. Đây chỉ là việc nhỏ thôi..."* — và nhận ra một điều đơn giản: **nếu ranh giới chỉ nằm trong lời văn, thì nó có thể bị lời văn khác nói cho biến mất.**

**Tôi sửa:** Tách ranh giới thành ba lớp, và ghi rõ lớp nào là gì:

| Lớp | Là gì | Sức mạnh |
|---|---|---|
| **L1** — System prompt | Chỉ thị cho LLM | **Lời khuyên.** Có thể bị thuyết phục. |
| **L2** — Post-validator trong code | Kiểm tra và ghi đè output của LLM | **Luật.** Không thương lượng được. |
| **L3** — Cổng gửi tin | Từ chối mọi payload còn thẻ `[DRAFT_ONLY]` | **Khoá vật lý.** AI không có đường đi qua. |

Và tôi đổi luôn cách viết assertion: các bài test bây giờ kiểm tra **đầu ra cuối cùng của hệ thống** (sau L2), chứ không kiểm tra raw output của LLM. Vì thứ chạm được vào cư dân là đầu ra của hệ thống, không phải câu trả lời của model.

---

### ❌ Sai #5 — Thiên hướng "chọn kiến trúc cho oai"

Khi tôi hỏi nên dùng kiến trúc nào, AI có xu hướng nghiêng về **Agentic Loop** — nghe hiện đại hơn. Tôi hỏi ngược lại: *"Agent cần tự lập kế hoạch. Trong quy trình này có bước nào cần lập kế hoạch không?"* Câu trả lời là không — tổ nào làm gì, SLA bao nhiêu đều đã được BQL quy định sẵn. Cái cần là **ánh xạ đúng**, không phải **sáng tạo**.

Tôi chốt **LLM Feature**, và giữ lớp Rule ở lại nhưng đổi vai: từ bộ phân loại chính thành **lớp chặn khẩn cấp + lưới an toàn khi LLM sập**. Inspiration Kit của Lab nói đúng: *"Problem First, AI Second"* — và tôi suýt làm ngược lại.

---

## 4. Ranh giới tôi tự đặt cho việc dùng AI

Trong buổi này tôi tự đặt ba nguyên tắc và giữ được cả ba:

1. **AI không được đặt con số vào báo cáo của tôi.** Mọi con số phải đi kèm `[S]` / `[E]` / `[M]`. Nếu không xếp được vào ô nào, con số đó bị xoá.
2. **AI không được là người cuối cùng đọc code của tôi.** Code phải chạy, test phải đỏ được ít nhất một lần trước khi tôi tin là nó xanh có ý nghĩa.
3. **AI không được chọn phạm vi dự án thay tôi.** AI đưa lựa chọn; lý do chọn phải là lý do tôi tự bảo vệ được trước một người phản đối.

---

## 5. Điều tôi mang đi

Trước buổi Lab, tôi nghĩ thiết kế một tính năng AI chủ yếu là viết một prompt đủ khéo. Sau buổi Lab, tôi nghĩ khác: **phần khó không phải làm cho AI làm được việc, mà là quyết định chỗ nào AI không được phép đụng vào — rồi thi hành quyết định đó bằng code chứ không bằng lời.**

Và điều khiến tôi nhớ lâu nhất không phải là một kiến trúc hay một metric. Đó là chữ **"khỏi"** — một chữ tiếng Việt rất đỗi bình thường, đủ sức biến một phiếu phàn nàn karaoke thành một báo động cháy. Không có buổi chạy thử đó, tôi đã nộp một hệ thống trông rất chỉn chu và sẽ hỏng trong tuần đầu tiên vận hành.

*Có những bug chỉ chịu xuất hiện khi ta bấm Run.*
