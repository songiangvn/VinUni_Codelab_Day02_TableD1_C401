# 01 — Problem Scan & Quick Cards
### Lab 02: AI Product Scoping — Vin Smart Future
**Mảng kinh doanh lựa chọn:** 🏢 **Vinhomes** — Quản lý vận hành đô thị (Smart Cities)
**Bài toán nhóm chọn:** Phân loại & Điều hướng phản ánh cư dân trên App Vinhomes Resident

---

## 📌 Quy ước ký hiệu độ tin cậy của số liệu

Mọi con số trong bài đều được gắn nhãn nguồn. Nhóm cố ý làm việc này vì rubric yêu cầu *"metric có số"* — nhưng một con số không rõ nguồn gốc thì tệ hơn là không có số.

| Nhãn | Ý nghĩa |
|:---:|---|
| **[S]** | **Sourced** — có nguồn công khai kiểm chứng được, có link. |
| **[E]** | **Estimated** — nhóm ước lượng theo benchmark ngành / suy luận có lập luận. Ghi rõ cách tính. |
| **[M]** | **Must-measure** — CHƯA có số. Đây là việc phải đo trong tuần đầu của dự án, không được đoán. |

> ⚠️ Nhóm **không** bịa số liệu nội bộ của Vinhomes. Những gì chúng tôi không biết, chúng tôi ghi **[M]** và kèm phương pháp đo.

---

# 🔍 Phase 1 — SCAN: Quét cơ hội bằng 4 Lenses

Nhóm rà soát vận hành của các công ty thành viên Vingroup và ghi nhận **7 bài toán** thực tế:

| # | Subsidiary | Lens | Mô tả ngắn bài toán | Tần suất ước tính |
|---|---|---|---|---|
| **1** | **Vinhomes** | **Lặp lại** | **Phân loại & điều hướng phản ánh cư dân.** Nhân viên CSKH của BQL đọc tay từng phiếu tiếng Việt tự do gửi qua App Vinhomes Resident, tự đoán phiếu thuộc tổ nào (Điện / Nước / Vệ sinh / An ninh / Thang máy...), tự gán mức ưu tiên bằng cảm tính, rồi chuyển tay sang tổ chuyên môn. | Hàng trăm phiếu/ngày/phân khu **[E]** |
| 2 | Vinhomes | Tốn thời gian | **Soạn tin phản hồi cư dân.** Sau khi tổ kỹ thuật xử lý xong, CSKH phải tự gõ tin đóng phiếu. Thực tế là copy-paste template cứng → cư dân cảm thấy "trả lời máy móc, cho có". | Mỗi phiếu đều phải soạn |
| 3 | Vinhomes | AI-upgrade | **Trợ lý thủ tục hành chính.** Cư dân muốn đăng ký thi công nội thất / vé gửi xe tháng / đăng ký khách phải hỏi BQL từng bước, BQL trả lời lặp lại cùng một nội dung hàng chục lần/tuần. | Cao, theo mùa |
| 4 | Xanh SM | Tốn thời gian | Điều phối viên xử lý thủ công sự cố pin/va chạm thực địa của tài xế (tra vị trí → tra trạm sạc trống → soạn chỉ dẫn). | ~80 sự cố/ngày HN (theo ví dụ mẫu của Lab) |
| 5 | VinFast | Lặp lại | Đối chiếu hóa đơn sạc điện hằng tuần giữa log trụ sạc đối tác và hệ thống tài chính. | Hằng tuần, khối lượng lớn |
| 6 | Vinmec | Pain từ người khác | Bác sĩ mất 20–30 phút/bệnh nhân để soạn tóm tắt hồ sơ xuất viện từ bệnh án điện tử. | Mỗi ca xuất viện |
| 7 | Vinpearl | Pain từ người khác | Quét review Booking/Agoda/Google Map để lọc ra phàn nàn khẩn cấp gửi Manager. | Hàng nghìn review/tháng |

### 🎯 Nhận xét sau khi quét

Ba quan sát định hình lựa chọn của nhóm:

1. **Bài toán #1 và #2 không phải hai bài toán — chúng là hai nửa của cùng một quy trình.** Cùng một phiếu, cùng một nhân viên, chỉ khác thời điểm (đầu luồng và cuối luồng). Tách ra làm hai dự án là sai về mặt sản phẩm.
2. **#1 là bài toán "ngôn ngữ tự nhiên tiếng Việt thuần tuý"** — đây chính xác là chỗ rule-based thua và LLM thắng. Cư dân không gõ theo form; họ gõ *"nhà tắm bốc mùi lạ từ cống lên mấy hôm nay"* (→ Thoát nước, không phải Vệ sinh) hoặc *"đèn hành lang tầng 12 chớp chớp như ma"* (→ Điện).
3. **#1 có ranh giới an toàn thú vị và khó** — có những phiếu tuyệt đối không được để AI tự quyết (mùi gas, kẹt thang máy, cháy). Một bài toán mà ranh giới dễ vẽ thì không học được gì.

---

# 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

## Card #1 — Phân loại & Điều hướng phản ánh cư dân ⭐ *(nhóm chọn)*

```text
┌──────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                            │
│                                                                  │
│ Bài toán (1 câu): Phiếu phản ánh của cư dân gửi qua App          │
│ Vinhomes Resident đang được CSKH của BQL đọc tay, đoán tổ        │
│ nghiệp vụ và gán ưu tiên thủ công → chậm, sai tổ, và quá tải     │
│ vào khung giờ tối.                                               │
│                                                                  │
│ Công ty thành viên: [x] Vinhomes                                 │
│                                                                  │
│ Ai đang đau (Actor)?                                             │
│   • CSKH/Trực ban của BQL tòa nhà — người gánh việc triage       │
│   • Cư dân — người chờ, và phải nhắc lại lần 2, lần 3            │
│   • Tổ kỹ thuật — nhận nhầm phiếu không thuộc chuyên môn         │
│                                                                  │
│ Workflow thủ công hiện tại (6 bước):                             │
│   1. Cư dân gõ mô tả tự do + ảnh trên App                        │
│ → 2. Phiếu rơi vào hàng đợi chung của BQL, CHỜ người đọc  🔴     │
│ → 3. CSKH đọc, gọi lại xác minh nếu mô tả thiếu thông tin        │
│ → 4. CSKH tự đoán tổ + tự gán ưu tiên, nhập hệ thống      🔴     │
│ → 5. Chuyển tổ chuyên môn (sai tổ thì đẩy ngược lại)      🔴     │
│ → 6. Xử lý xong, CSKH gõ tay tin phản hồi đóng phiếu      🔴     │
│                                                                  │
│ Bước nào tốn thời gian/lỗi nhất?                                 │
│   Bước 2–4 (chờ + đọc + đoán tổ): ⏱ ~4 phút công/phiếu **[E]**,  │
│   cộng thời gian NẰM CHỜ trong hàng đợi (đây mới là phần lớn      │
│   của con số "12 tiếng" mà cư dân cảm nhận).                     │
│                                                                  │
│ AI có thể nhảy vào hỗ trợ ở bước nào?                            │
│   Bước 2–4: đọc mô tả tiếng Việt tự do → trả về nhãn (category,  │
│   sub-category), mức ưu tiên P0–P3, tổ tiếp nhận, kèm            │
│   confidence + margin. Bước 6: draft tin phản hồi (có gắn thẻ    │
│   [DRAFT_ONLY], CSKH bấm duyệt mới gửi).                         │
│                                                                  │
│ Đo thành công bằng gì (Metric có số)?                            │
│   1. Top-1 routing accuracy ≥ 92%, macro-F1 ≥ 0.85 trên gold set │
│      500 phiếu (vì các lớp rất mất cân bằng).                    │
│   2. Time-to-assign: P90 từ ~45 phút giờ cao điểm → ≤ 60 giây.   │
│   3. Tỉ lệ route sai: 12% **[E]** → ≤ 5%.                        │
│   4. 🚨 CHẶN GO-LIVE: 0 phiếu khẩn cấp (P0) bị hạ nhãn thành     │
│      non-P0 trên gold set. Không đánh đổi.                       │
│                                                                  │
│ Quick Architecture: [ ] No AI  [x] Rule (lớp chặn) [x] LLM       │
│                     [ ] Agent  → Hybrid: Rule guard + LLM Feature│
└──────────────────────────────────────────────────────────────────┘
```

---

## Card #2 — Soạn tin phản hồi đóng phiếu cho cư dân

```text
┌──────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                            │
│                                                                  │
│ Bài toán (1 câu): CSKH phải tự gõ tin phản hồi cho từng phiếu    │
│ đã xử lý xong; thực tế dùng template cứng nên cư dân đánh giá    │
│ là "trả lời rập khuôn, không giải quyết vấn đề của tôi".         │
│                                                                  │
│ Công ty thành viên: [x] Vinhomes                                 │
│                                                                  │
│ Ai đang đau? CSKH (gõ lặp lại), Cư dân (nhận tin vô hồn),        │
│              BQL (điểm hài lòng CSAT thấp)                       │
│                                                                  │
│ Workflow thủ công hiện tại (4 bước):                             │
│   1. Tổ kỹ thuật báo đã xử lý xong (thường là 1 dòng ngắn)       │
│ → 2. CSKH mở phiếu gốc đọc lại cư dân phản ánh gì                │
│ → 3. CSKH chọn template gần đúng nhất và sửa vài chữ      🔴     │
│ → 4. Gửi qua App, đóng phiếu                                     │
│                                                                  │
│ Bước nào tốn nhất? Bước 3 (⏱ ~5 phút/phiếu **[E]**)              │
│ AI có thể nhảy vào ở bước nào? Bước 3 — draft tin phản hồi từ    │
│ (phiếu gốc + ghi chú xử lý của tổ kỹ thuật), giọng văn thân      │
│ thiện, có nêu đúng việc đã làm.                                  │
│                                                                  │
│ Đo thành công bằng gì?                                           │
│   Giảm thời gian soạn phản hồi 5 phút → dưới 1 phút;             │
│   tỉ lệ CSKH chấp nhận draft không sửa ≥ 70%.                    │
│                                                                  │
│ Quick Architecture: [ ] No AI [ ] Rule [x] LLM  [ ] Agent        │
└──────────────────────────────────────────────────────────────────┘
```

**➡️ Kết luận về Card #2:** Đây **không phải một dự án riêng**. Nó dùng chung nguồn dữ liệu (phiếu phản ánh), chung người dùng (CSKH), chung màn hình. Nhóm quyết định **gộp Card #2 vào làm Phase 2 của cùng một sản phẩm** với Card #1, thay vì mở hai dự án song song.

---

## Card #3 — Trợ lý cư dân hỗ trợ thủ tục hành chính

```text
┌──────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                            │
│                                                                  │
│ Bài toán (1 câu): Cư dân muốn đăng ký thi công nội thất, vé gửi  │
│ xe tháng, đăng ký khách... phải hỏi BQL từng bước; BQL trả lời   │
│ lặp lại cùng một nội dung hàng chục lần mỗi tuần.                │
│                                                                  │
│ Công ty thành viên: [x] Vinhomes                                 │
│                                                                  │
│ Ai đang đau? Cư dân (không biết cần giấy tờ gì), BQL (trả lời    │
│              lặp), Tổ hành chính (hồ sơ nộp thiếu → trả lại)     │
│                                                                  │
│ Workflow thủ công hiện tại (4 bước):                             │
│   1. Cư dân nhắn/gọi/xuống quầy hỏi thủ tục                      │
│ → 2. BQL đọc lại quy định, liệt kê giấy tờ cần nộp        🔴     │
│ → 3. Cư dân nộp hồ sơ, thường thiếu 1–2 giấy tờ           🔴     │
│ → 4. BQL trả hồ sơ, cư dân làm lại (lặp vòng 2–3 lần)            │
│                                                                  │
│ Bước nào tốn nhất? Bước 2–3, và đặc biệt là VÒNG LẶP ở bước 4.   │
│ AI có thể nhảy vào ở bước nào? Bước 2 (RAG trên bộ quy định      │
│ nội khu) + Bước 3 (checklist hồ sơ tự sinh).                     │
│                                                                  │
│ Đo thành công bằng gì?                                           │
│   Giảm tỉ lệ hồ sơ nộp thiếu giấy tờ từ ~40% **[M]** → ≤ 15%.    │
│                                                                  │
│ Quick Architecture: [ ] No AI [ ] Rule [x] LLM + RAG [ ] Agent   │
└──────────────────────────────────────────────────────────────────┘
```

---

# 🗳️ Quyết định lựa chọn của nhóm

> ### ✅ Nhóm chọn **Card #1 — Phân loại & Điều hướng phản ánh cư dân**, và **gộp Card #2** làm giai đoạn 2 của cùng sản phẩm.

### Vì sao chọn #1

| Tiêu chí | Lý giải |
|---|---|
| **Đúng bản chất bài toán AI** | Input là **tiếng Việt tự do, không dấu, sai chính tả, mô tả gián tiếp**. Đây là vùng mà keyword-rule sập và LLM thắng rõ rệt. Không phải chọn AI vì "cho sang". |
| **Bottleneck là thật và đo được** | Mọi phiếu đều phải đi qua bước triage. Không có đường vòng. Cải thiện ở đây là cải thiện toàn bộ luồng. |
| **Ranh giới an toàn khó và đáng học** | Có lớp phiếu (cháy, gas, kẹt thang máy) mà **sai một lần là hỏng cả dự án**. Buộc nhóm phải thiết kế ranh giới nghiêm túc, không chỉ viết prompt cho vui. |
| **Rủi ro có thể chặn được** | AI chỉ *gợi ý nhãn* và *draft tin*; con người vẫn bấm duyệt. Không có hành động vật lý nào do AI tự khởi tạo. |
| **Chi phí triển khai thấp** | Không cần fine-tune, không cần hạ tầng mới, chỉ cần một service phân loại đứng giữa App và hệ thống vận hành hiện có. |

### Vì sao loại các thẻ còn lại

- **Card #2 — không loại, mà gộp.** Nó là phần đuôi của cùng một luồng. Làm riêng sẽ tạo ra hai đội, hai backlog, hai lần tích hợp cho cùng một màn hình của CSKH.
- **Card #3 — hoãn (Not Yet).** Bài toán này cần một **kho quy định nội khu sạch, có phiên bản, khác nhau giữa từng khu đô thị** để làm RAG. Kho đó hiện chưa tồn tại ở dạng máy đọc được **[M]**. Làm RAG trên tài liệu chưa được chuẩn hoá = chatbot bịa quy định = rủi ro tranh chấp với cư dân. Phải chuẩn hoá dữ liệu trước, không phải chuẩn hoá prompt trước.
- **Các bài toán ngoài Vinhomes (#4–#7) — loại vì không ai trong nhóm hiểu quy trình thực tế.** Theo đúng lưu ý của Inspiration Kit: *"Hãy ưu tiên chọn bài toán mà ít nhất một thành viên hiểu rõ quy trình hiện tại."* Nhóm có thành viên đang sống trong khu đô thị Vinhomes và đã từng gửi phản ánh qua App — đó là lợi thế thông tin thật, không nên vứt đi.

---

## 🧨 Nhóm tự phản biện (Stress-test theo vai CFO & Trưởng phòng Vận hành)

Nhóm đã chủ động đóng vai người phản đối dự án. Ba đòn mạnh nhất và câu trả lời:

**1. "Chỉ cần cho cư dân chọn dropdown danh mục trên App là xong. Tốn gì AI?"**
> Đòn này đúng một phần và nhóm thừa nhận: **dropdown phải được làm, và làm trước.** Nhưng dropdown không giải quyết ba thứ: (a) cư dân chọn sai hoặc chọn bừa "Khác" — mục "Khác" luôn phình to trong mọi hệ thống ticket; (b) một phiếu thường chứa nhiều vấn đề ("nước yếu **và** đèn hành lang hỏng"); (c) mức độ khẩn cấp không nằm ở danh mục mà nằm ở **câu chữ** ("có mùi khét" so với "đèn hơi mờ" cùng thuộc mục Điện). AI xử lý phần *sau* dropdown, không thay thế dropdown.

**2. "Rule-based keyword là đủ. Chỉ cần map 'mất nước' → tổ Nước."**
> Nhóm đã **đo thật** thay vì đoán: tự gán nhãn 30 phiếu tiếng Việt rồi chạy rule qua — được **80% đúng, 20% chuyển người, 0% route sai** *sau khi sửa hai bug mà chính phép đo đó phơi ra* (chi tiết ở [02-deep-dive-report.md](02-deep-dive-report.md)). n=30 quá nhỏ để kết luận, nên con số thật vẫn là **[M]** trên gold set 500 phiếu. Phần rule sập là phần đắt nhất: mô tả gián tiếp (*"trần nhà vệ sinh ố vàng nhỏ giọt"* → Thấm/Nước, không có từ khoá "nước"), không dấu (*"mat nuoc tu sang"*), teencode, và phiếu đa vấn đề. Quan trọng hơn: **rule không biết nó đang sai.** LLM có thể trả về confidence + margin để hệ thống tự biết lúc nào nên nhường cho người. Đó là thứ nhóm mua, không phải "độ thông minh".

**3. "AI phân loại sai một phiếu báo cháy thì ai chịu trách nhiệm?"**
> Đây là đòn đúng nhất và nó **định hình toàn bộ thiết kế**. Câu trả lời của nhóm không phải "AI sẽ chính xác lắm", mà là **rút lớp phiếu đó ra khỏi quyền quyết định của AI**: một lớp rule cứng (regex + từ khoá khẩn cấp) chạy **trước** LLM; hễ khớp là phiếu đi thẳng lên Trung tâm điều hành và hotline 24/7, LLM không có quyền hạ cấp nó. Ngoài ra metric chặn go-live của nhóm là **0 phiếu P0 bị hạ nhãn** — nếu gold set cho thấy dù chỉ 1 ca, dự án không được bật auto-route. Rủi ro ở đây là **bất đối xứng**, nên ngưỡng cũng phải bất đối xứng.

---

*Chi tiết phân tích sâu, sơ đồ quy trình, Problem Statement 6-field và quyết định Go/No-Go: xem [02-deep-dive-report.md](02-deep-dive-report.md).*
