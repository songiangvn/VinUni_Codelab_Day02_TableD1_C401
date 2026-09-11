# Phase 1 — SCAN: Tìm kiếm cơ hội AI cho Vin Smart Future

> **Phạm vi:** Quét hỗn hợp các mảng VinFast, Xanh SM, Vinhomes và Vinmec bằng bốn lenses trong worksheet.
>
> **Nguyên tắc về số liệu:** Tài liệu này **không đưa ra số tổn thất, thời gian, chi phí hay tỷ lệ ước tính** khi chưa có dữ liệu nội bộ đã được xác minh. Các nội dung dưới đây là **problem hypotheses** để phỏng vấn stakeholder và đo baseline, không phải kết luận rằng quy trình hiện tại chắc chắn đang diễn ra đúng như mô tả.

---

## Danh sách bài toán của tôi

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|---|---|---|
| 1 | **VinFast** | **AI có thể tốt hơn** | **Giả thuyết:** Cố vấn dịch vụ có thể phải đọc mô tả lỗi xe bằng ngôn ngữ tự nhiên, hỏi lại, tra tài liệu và phân loại trước khi tạo phiếu sửa chữa; mô tả mơ hồ có thể làm sai tuyến xử lý và phát sinh trao đổi lại. |
| 2 | **VinFast** | **Lặp lại** | **Giả thuyết:** Nhân sự vận hành có thể phải đối soát ngoại lệ giữa phiên sạc, chính sách ưu đãi, giao dịch thanh toán và chứng từ đối tác hạ tầng; mỗi sai lệch có thể đòi hỏi mở nhiều hệ thống và lần lại dữ liệu. |
| 3 | **Xanh SM** | **Pain từ người khác** | **Giả thuyết:** Nhân viên CSKH/vận hành có thể phải tổng hợp cuộc gọi, ghi chú tài xế và log chuyến để xác định nguyên nhân hủy hoặc khiếu nại; phân loại thiếu nhất quán có thể khiến các bên chờ và che khuất nguyên nhân gốc. |
| 4 | **Vinhomes** | **Lặp lại** | **Giả thuyết:** Nhân viên CSKH/Ban Quản lý có thể phải đọc phản ánh tự do, xác định địa điểm, nhóm sự cố và đơn vị phụ trách rồi chuyển ticket; yêu cầu thiếu thông tin hoặc chuyển sai đội có thể gây vòng lặp xử lý. |
| 5 | **Vinmec** | **Tốn thời gian** | **Giả thuyết:** Bác sĩ có thể phải tổng hợp diễn biến điều trị từ nhiều phần của hồ sơ để soạn tóm tắt xuất viện; việc tìm, chọn và diễn đạt lại thông tin có thể lấn vào thời gian trao đổi trực tiếp với người bệnh. |

---

## Chi tiết các problem hypotheses

### Problem 1 — VinFast: Phân loại mô tả lỗi xe và chuẩn bị phiếu dịch vụ

- **Actor cần phỏng vấn:** Khách hàng, nhân viên tổng đài, cố vấn dịch vụ và kỹ thuật viên tại xưởng.
- **Workflow thủ công giả định:** Khách mô tả hiện tượng → nhân viên hỏi lại → tra cứu hướng dẫn/mã nhóm lỗi → xác định mức ưu tiên và xưởng phù hợp → nhập lại nội dung vào phiếu dịch vụ.
- **Bottleneck:** Mô tả tiếng Việt tự do có thể thiếu bối cảnh, dùng từ tượng thanh hoặc không trùng với thuật ngữ kỹ thuật. Cùng một hiện tượng có thể được diễn đạt theo nhiều cách.
- **Rò rỉ hiệu suất có thể xảy ra:** Liên hệ lại nhiều lần, tạo phiếu thiếu dữ liệu, chuyển sai hàng đợi, kỹ thuật viên phải khai thác lại từ đầu và lịch hẹn bị kéo dài.
- **Cơ hội AI:** LLM có thể chuẩn hóa mô tả thành bản nháp có cấu trúc, gợi ý câu hỏi còn thiếu và đề xuất nhóm dịch vụ. Rule engine nên xử lý các cờ an toàn rõ ràng.
- **Ranh giới sơ bộ:** AI không được kết luận nguyên nhân hỏng hóc, khẳng định xe an toàn để tiếp tục chạy, hay tự phê duyệt sửa chữa/bảo hành. Các dấu hiệu liên quan đến an toàn phải được chuyển ngay cho con người theo quy tắc định sẵn.
- **Dữ liệu cần thu thập để xác lập baseline:** Nội dung liên hệ ban đầu; số lần hỏi lại; lịch sử đổi tuyến; thời điểm mở/đóng phiếu; tỷ lệ phiếu bị mở lại; đánh giá của cố vấn dịch vụ về độ đầy đủ của thông tin.

**Căn cứ bối cảnh:** Hướng dẫn chính thức cho thấy khách hàng có thể chọn loại dịch vụ, thêm mô tả chi tiết và gửi yêu cầu để xưởng tiếp nhận, xác nhận. Trang đặt lịch cũng có trường ghi chú và ảnh đính kèm. Các nguồn chỉ xác nhận điểm chạm đầu vào; chưa chứng minh việc phân loại hiện tại là thủ công hay bottleneck đã tồn tại. Xem [hướng dẫn tiện ích dịch vụ trên ứng dụng VinFast](https://vinfastauto.com/vn_vi/huong-dan-su-dung-tien-ich-dich-vu-tren-ung-dung-vinfast) và [trang đặt lịch dịch vụ VinFast](https://shop.vinfastauto.com/vn_vi/dat-lich-dich-vu-bao-duong.html).

### Problem 2 — VinFast: Đối soát ngoại lệ của phiên sạc và chứng từ đối tác

- **Actor cần phỏng vấn:** Nhân viên vận hành trạm sạc, kế toán đối soát và nhân sự quản lý đối tác.
- **Workflow thủ công giả định:** Nhận danh sách ngoại lệ → mở log phiên sạc → kiểm tra quyền lợi/ưu đãi → đối chiếu giao dịch và chứng từ → liên hệ đơn vị liên quan → ghi nhận cách xử lý.
- **Bottleneck:** Dữ liệu liên quan nằm ở nhiều nguồn và có thể khác mã định danh, thời điểm ghi nhận hoặc trạng thái. Nhân viên phải lặp lại cùng một chuỗi kiểm tra cho từng ngoại lệ.
- **Rò rỉ hiệu suất có thể xảy ra:** Backlog đối soát, thanh toán đối tác chậm, mất thời gian truy vết, một lỗi có thể được xử lý thiếu nhất quán giữa các nhân viên.
- **Cơ hội AI:** Trước hết dùng rule-based matching cho trường hợp xác định; dùng anomaly detection để ưu tiên ngoại lệ; chỉ dùng LLM để tóm tắt bằng chứng và soạn bản giải thích cho người duyệt.
- **Ranh giới sơ bộ:** AI không được tự điều chỉnh sổ kế toán, tự xác nhận công nợ, tự hoàn tiền hoặc thay đổi quyền lợi khách hàng. Mọi bút toán và quyết định tài chính phải do người có thẩm quyền duyệt.
- **Dữ liệu cần thu thập để xác lập baseline:** Số lượng ngoại lệ theo loại; thời gian từ lúc phát hiện đến lúc đóng; số hệ thống phải truy cập; số lần chuyển người xử lý; nguyên nhân gốc; giá trị giao dịch đang chờ đối soát; lịch sử điều chỉnh sau duyệt.

**Căn cứ bối cảnh:** Hồ sơ công bố của VinFast mô tả quan hệ dịch vụ trạm sạc với V-Green; trang chính thức về mô hình trạm sạc nhượng quyền xác nhận có thêm bên vận hành hạ tầng. Đây chỉ là căn cứ để khảo sát xem có luồng ngoại lệ liên tổ chức đáng kể hay không; nguồn không công bố cách đối soát, mức độ thủ công hoặc tổn thất. Xem [VinFast Form 20-F trên SEC](https://www.sec.gov/Archives/edgar/data/1913510/000110465926052266/vfs-20251231x20f.htm) và [giới thiệu mô hình trạm sạc nhượng quyền](https://vinfastauto.com/vn_vi/v-green-tien-phong-trien-khai-mo-hinh-tram-sac-nhuong-quyen-tai-viet-nam).

### Problem 3 — Xanh SM: Tổng hợp và phân loại nguyên nhân hủy chuyến/khiếu nại

- **Actor cần phỏng vấn:** Khách hàng, tài xế, nhân viên CSKH, điều phối viên và quản lý chất lượng dịch vụ.
- **Workflow thủ công giả định:** Tiếp nhận phản ánh → nghe/đọc nội dung → mở log chuyến và ghi chú tài xế → đối chiếu hai phía → gán nguyên nhân → chuyển người có thẩm quyền xử lý.
- **Bottleneck:** Bằng chứng gồm dữ liệu có cấu trúc và nội dung tự do từ nhiều phía; cách đặt nhãn nguyên nhân có thể khác nhau giữa nhân viên.
- **Rò rỉ hiệu suất có thể xảy ra:** Khách và tài xế chờ lâu, xử lý thiếu nhất quán, khiếu nại bị chuyển vòng, báo cáo nguyên nhân gốc không phản ánh đúng vấn đề của vận hành.
- **Cơ hội AI:** Speech-to-text và LLM có thể tóm tắt hai phía, trích xuất dữ kiện, gợi ý taxonomy nguyên nhân và dẫn lại bằng chứng; rules kiểm tra các điều kiện chính sách.
- **Ranh giới sơ bộ:** AI không được tự quy lỗi cho tài xế/khách hàng, tự khóa tài khoản, tự áp dụng chế tài hoặc tự quyết định hoàn tiền. Trường hợp tranh chấp và an toàn phải có người xem xét.
- **Dữ liệu cần thu thập để xác lập baseline:** Log chuyến; ghi âm/transcript; ghi chú hai phía; lịch sử gán và đổi nhãn; thời điểm qua từng hàng đợi; số lần chuyển tuyến; kết quả xử lý cuối; phản hồi sau xử lý.

**Căn cứ bối cảnh:** Green SM công khai một chương trình tiếp nhận phản ánh tại thị trường Indonesia, cho phép khách gửi kèm hình ảnh/tài liệu và có bộ phận chuyên trách xác minh, phân loại, phản hồi. Nguồn này chỉ xác nhận loại điểm chạm nghiệp vụ trong hệ thống Green SM; không chứng minh quy trình tại Việt Nam giống hệt, đang làm thủ công hay đang gây bottleneck. Xem [chương trình lắng nghe góp ý khách hàng của Green SM](https://www.vingroup.net/vi/tin-tuc-su-kien/bai-viet/8037/green-sm-launches-customer-feedback-programme-reaffirming-its-commitment-to-enhancing-service-quality).

### Problem 4 — Vinhomes: Phân loại và điều hướng phản ánh của cư dân

- **Actor cần phỏng vấn:** Cư dân, nhân viên CSKH, Ban Quản lý và các đội kỹ thuật, an ninh, vệ sinh/cảnh quan.
- **Workflow thủ công giả định:** Cư dân gửi phản ánh → CSKH đọc và xác minh vị trí → yêu cầu bổ sung thông tin → chọn nhóm vấn đề/độ khẩn cấp → chuyển đội phụ trách → theo dõi phản hồi.
- **Bottleneck:** Nội dung tự do có thể chứa nhiều yêu cầu, thiếu vị trí hoặc dùng tên gọi không chính thức; trách nhiệm xử lý phụ thuộc khu đô thị, tòa nhà và loại tài sản.
- **Rò rỉ hiệu suất có thể xảy ra:** Ticket chuyển sai đội, phải hỏi lại, vi phạm SLA nội bộ, công việc hiện trường bị trùng lặp và cư dân mất niềm tin vì không biết trạng thái xử lý.
- **Cơ hội AI:** LLM trích xuất vị trí/vấn đề từ phản ánh và ảnh đính kèm, gợi ý câu hỏi bổ sung; rule engine ánh xạ sang đơn vị phụ trách và mức ưu tiên theo sổ tay vận hành.
- **Ranh giới sơ bộ:** AI không được tự cam kết bồi thường, kết luận trách nhiệm pháp lý, đóng ticket khi cư dân chưa được phản hồi hoặc trì hoãn tình huống khẩn cấp. Các từ khóa an toàn phải kích hoạt luồng khẩn cấp dựa trên rules.
- **Dữ liệu cần thu thập để xác lập baseline:** Nội dung ticket; metadata vị trí; lịch sử chuyển đội; lý do yêu cầu bổ sung; thời điểm ở từng trạng thái; số lần mở lại; mức hài lòng sau xử lý; taxonomy sự cố hiện có.

**Căn cứ bối cảnh:** Vinhomes xác nhận ứng dụng cư dân hỗ trợ đăng ký dịch vụ và giao tiếp với Ban Quản lý/CSKH; điều này tạo một điểm vào phù hợp để khảo sát bài toán phân loại ticket. Nguồn không xác nhận rằng việc route hiện nay hoàn toàn thủ công. Xem [trang chính thức về tiện ích cư dân Vinhomes](https://vinhomes.vn/vi) và [giới thiệu ứng dụng Vinhomes Resident](https://vinhomes.vn/vi/nhung-la-thu-cam-on-tu-cu-dan-va-dich-vu-tu-trai-tim-vinhomes).

### Problem 5 — Vinmec: Soạn bản nháp tóm tắt xuất viện

- **Actor cần phỏng vấn:** Bác sĩ điều trị, điều dưỡng, nhân viên quản lý hồ sơ và người bệnh/người chăm sóc.
- **Workflow thủ công giả định:** Mở hồ sơ bệnh án → rà diễn biến, xét nghiệm, thủ thuật và thuốc → chọn sự kiện quan trọng → viết tóm tắt và hướng dẫn → kiểm tra lại → ký xác nhận.
- **Bottleneck:** Thông tin nằm ở nhiều phần của hồ sơ, có nội dung lặp hoặc thay đổi theo thời gian; bác sĩ phải vừa tổng hợp chính xác vừa diễn đạt dễ hiểu.
- **Rò rỉ hiệu suất có thể xảy ra:** Bác sĩ dành ít thời gian hơn cho tư vấn trực tiếp, hồ sơ hoàn tất chậm, thiếu thông tin khi chuyển tiếp chăm sóc và nhân viên phải gọi lại để làm rõ.
- **Cơ hội AI:** LLM đặt trong môi trường dữ liệu được kiểm soát có thể tạo bản nháp có trích dẫn về đúng vị trí trong hồ sơ, đánh dấu mâu thuẫn/thiếu dữ kiện và chờ bác sĩ chỉnh sửa.
- **Ranh giới sơ bộ:** AI không được tự thêm chẩn đoán, thay đổi thuốc, tạo chỉ định, che giấu thông tin mâu thuẫn hoặc ký/phát hành bản tóm tắt. Bác sĩ chịu trách nhiệm kiểm tra và phê duyệt toàn bộ nội dung.
- **Dữ liệu cần thu thập để xác lập baseline:** Audit log thao tác hồ sơ; thời gian bắt đầu/ký; số nguồn được mở; mức độ chỉnh sửa sau bản nháp; trường thông tin hay thiếu; số lần hồ sơ bị trả lại; phản hồi của bác sĩ và người nhận bản tóm tắt.

**Căn cứ bối cảnh:** Hướng dẫn nội trú chính thức của Vinmec xác nhận người bệnh nhận báo cáo xuất viện cùng các kết quả và đơn thuốc. Nghiên cứu gốc chỉ được dùng để củng cố tính hợp lý của hướng khảo sát về documentation, không được dùng để suy ra quy trình, thời gian hoặc tổn thất riêng của Vinmec. Xem [hướng dẫn điều trị nội trú tại Vinmec](https://www.vinmec.com/eng/blog/guidelines-for-inpatient-treatment-at-vinmec), [nghiên cứu time-motion về quy trình xuất viện](https://pubmed.ncbi.nlm.nih.gov/28349373/) và [nghiên cứu về bác sĩ phối hợp với LLM khi tóm tắt diễn biến điều trị](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2837483).

---

## Cách xác minh trước khi chọn top problems cho Phase 2

Trước khi đưa một problem sang QUICK-ASSESS, cần thực hiện các bước sau:

- Phỏng vấn trực tiếp actor và người nhận đầu ra của quy trình.
- Quan sát một số case thực tế từ đầu đến cuối, bao gồm cả case bình thường và ngoại lệ.
- Trích log để dựng baseline từ dữ liệu thật thay vì hỏi cảm nhận chung.
- Xác định bước nào chỉ cần rule/workflow automation, bước nào thật sự cần xử lý ngôn ngữ hoặc dữ liệu phi cấu trúc bằng AI.
- Kiểm tra quyền truy cập dữ liệu, dữ liệu cá nhân và yêu cầu Human-in-the-loop trước khi đề xuất kiến trúc.

## Đề xuất thứ tự ưu tiên để mang sang QUICK-ASSESS

Không dùng số giả định để xếp hạng. Có thể ưu tiên phỏng vấn ba problem sau vì đầu ra đều có thể để ở chế độ **draft/gợi ý**, giữ quyết định cuối ở con người và có fallback về quy trình cũ:

- **Vinhomes — phân loại và điều hướng phản ánh cư dân.**
- **Xanh SM — tổng hợp và phân loại nguyên nhân hủy chuyến/khiếu nại.**
- **VinFast — chuẩn hóa mô tả lỗi và chuẩn bị phiếu dịch vụ.**

Vinmec cần kiểm soát dữ liệu và đánh giá an toàn nghiêm ngặt hơn; đối soát sạc nên ưu tiên rule-based matching trước khi cân nhắc dùng LLM.
