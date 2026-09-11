# 01 — Problem Scan: Ý tưởng cá nhân & nhóm

**Nhóm lựa chọn trọng tâm:** Vinhomes — Phân loại và điều hướng phản ánh cư dân từ App Vinhomes Resident.

---

## Phase 1 — SCAN: Bảng quét cơ hội

Dùng các “lenses” để tìm các tác vụ có tần suất cao, nhiều thao tác thủ công hoặc có thể tăng chất lượng nhờ AI.

| # | Công ty thành viên | Lens | Bài toán thực tế | Người đang gặp khó khăn | Cơ hội AI |
|---|---|---|---|---|---|
| 1 | **Vinhomes** | Lặp lại | Phân loại phản ánh cư dân như mất nước, hỏng đèn, rò rỉ, tiếng ồn, vệ sinh… gửi qua App Vinhomes Resident và chuyển đến đúng ban quản lý từng tòa. | Cư dân, CSKH, ban quản lý (BQL), đội kỹ thuật. | Đọc nội dung tự do, nhận diện loại sự cố, mức ưu tiên và đề xuất đúng hàng chờ xử lý. |
| 2 | **Xanh SM (GSM)** | Tốn thời gian | Điều phối viên xử lý báo cáo sự cố sạc pin hoặc va chạm từ tài xế trong giờ cao điểm. | Tài xế và điều phối viên. | Tóm tắt sự cố, trích xuất vị trí/loại xe và soạn bản nháp hướng dẫn hoặc lệnh điều phối. |
| 3 | **Vinmec** | Pain từ người khác | Bác sĩ phải viết tóm tắt hồ sơ xuất viện và hướng dẫn chăm sóc sau điều trị cho từng bệnh nhân. | Bác sĩ, điều dưỡng, bệnh nhân. | Tạo bản nháp tóm tắt từ hồ sơ có cấu trúc để bác sĩ kiểm tra, chỉnh sửa và ký duyệt. |
| 4 | **VinFast** | Lặp lại | Phân loại yêu cầu bảo hành và triệu chứng lỗi xe gửi từ khách hàng/đại lý. | Tổng đài, cố vấn dịch vụ, kỹ thuật viên. | Chuẩn hóa mô tả lỗi, gợi ý nhóm kỹ thuật và mức độ ưu tiên theo lịch sử lỗi. |
| 5 | **Vincom Retail** | Tốn thời gian | Tổng hợp phản hồi khách hàng từ quầy dịch vụ, mạng xã hội và biểu mẫu khảo sát để lập báo cáo định kỳ. | Ban quản lý trung tâm thương mại, CSKH. | Gom cụm chủ đề, phân tích cảm xúc và tạo báo cáo xu hướng kèm các vấn đề cần ưu tiên. |
| 6 | **Vinpearl** | AI-upgrade | Nhân viên CSKH trả lời lặp lại các câu hỏi về nhận/trả phòng, tiện ích, lịch xe đưa đón và chính sách dịch vụ. | Khách lưu trú và nhân viên CSKH. | Trợ lý trả lời theo knowledge base, chuyển cho nhân viên khi câu hỏi ngoài phạm vi hoặc có khiếu nại. |

---

## Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

Ba bài toán tiềm năng nhất được chọn để đánh giá nhanh là: **#1 Vinhomes**, **#2 Xanh SM** và **#3 Vinmec**.

### Quick Problem Card #1 — Vinhomes: Phân loại & điều hướng phản ánh cư dân

| Hạng mục | Nội dung |
|---|---|
| **Bài toán** | Tự động phân loại các khiếu nại/phản ánh của cư dân (mất nước, hỏng đèn, rò rỉ, tiếng ồn, vệ sinh, an ninh…) trên App Vinhomes Resident và chuyển đến đúng BQL tòa nhà hoặc đội chuyên môn. |
| **Actor / Operator** | Nhân viên CSKH tập trung; BQL từng tòa; đội kỹ thuật, bảo vệ và vệ sinh. |
| **Quy trình hiện tại** | 1) Cư dân gửi mô tả, ảnh và căn hộ/khu vực trên app. 2) CSKH đọc ticket và kiểm tra tòa nhà. 3) CSKH xác định loại sự cố, mức độ khẩn. 4) CSKH chuyển ticket cho BQL hoặc đội phụ trách. 5) BQL theo dõi và cập nhật cư dân. |
| **Bottleneck** | Nội dung phản ánh viết tự do, thường ngắn hoặc thiếu vị trí; nhân viên phải đọc và đối chiếu tòa nhà thủ công. Ticket có nhiều vấn đề dễ bị chuyển nhầm hoặc chuyển lại. Thời gian phân luồng khoảng 5–8 phút/ticket. |
| **AI Solution** | LLM trích xuất loại sự cố, địa điểm, mức độ ưu tiên và tín hiệu an toàn; rule-based router kiểm tra tòa nhà, nhóm nhận xử lý và các quy tắc khẩn cấp. AI chỉ đề xuất tuyến; ticket độ tin cậy thấp hoặc khẩn cấp phải có nhân sự xác nhận. |
| **Metric thành công** | Median time-to-route dưới 1 phút/ticket; độ chính xác phân loại/định tuyến ≥95%; 100% ticket có tín hiệu cháy nổ, ngập nghiêm trọng hoặc an ninh được gắn cờ khẩn; giảm ≥30% ticket phải chuyển lại. |
| **Rủi ro & boundary** | Không để AI tự đóng ticket, tự cam kết thời gian khắc phục hoặc hạ mức độ khẩn. Nếu thiếu tòa nhà/vị trí, yêu cầu bổ sung thông tin thay vì suy đoán. Chỉ sử dụng dữ liệu tối thiểu cần cho xử lý. |
| **Đánh giá nhanh** | **Ưu tiên cao.** Khối lượng lặp lại lớn, đầu vào sẵn có trên app, có KPI rõ và có thể pilot theo mô hình AI đề xuất + người duyệt. |

### Quick Problem Card #2 — Xanh SM: Xử lý sự cố sạc pin thực địa

| Hạng mục | Nội dung |
|---|---|
| **Bài toán** | Hỗ trợ điều phối viên xử lý các báo cáo xe sắp hết pin hoặc gặp sự cố sạc khi tài xế đang hoạt động. |
| **Actor / Operator** | Tài xế Xanh SM, điều phối viên, đội cứu hộ pin di động. |
| **Quy trình hiện tại** | 1) Tài xế gọi hoặc gửi báo cáo. 2) Điều phối viên tra GPS xe. 3) Mở dashboard tìm trạm sạc trống, phù hợp dòng xe. 4) Soạn hướng dẫn cho tài xế. 5) Gọi cứu hộ nếu cần. |
| **Bottleneck** | Phải chuyển đổi giữa bản đồ, dashboard trạm sạc và công cụ nhắn tin; việc tìm trạm tương thích và viết hướng dẫn thường mất 10–12 phút/lượt. |
| **AI Solution** | Tự kéo vị trí xe và dữ liệu trạm sạc, xếp hạng phương án phù hợp, tạo tin nhắn hướng dẫn ở dạng nháp. Rule engine bắt buộc gọi cứu hộ khi pin dưới ngưỡng an toàn. |
| **Metric thành công** | Giảm thời gian xử lý từ khoảng 15 phút xuống dưới 3 phút; ≥98% đề xuất đúng loại trụ sạc và đúng vị trí; không có đề xuất trạm vượt ngưỡng an toàn khi pin quá thấp. |
| **Rủi ro & boundary** | Không tự gửi tin nhắn hay điều xe cứu hộ nếu chưa có phê duyệt. Không đề xuất trạm xa khi pin dưới ngưỡng; ưu tiên an toàn giao thông. |
| **Đánh giá nhanh** | **Ưu tiên trung bình-cao.** Tác động vận hành trực tiếp nhưng phụ thuộc vào chất lượng dữ liệu GPS/trạm sạc thời gian thực. |

### Quick Problem Card #3 — Vinmec: Bản nháp tóm tắt xuất viện

| Hạng mục | Nội dung |
|---|---|
| **Bài toán** | Hỗ trợ bác sĩ tạo bản nháp tóm tắt hồ sơ xuất viện và hướng dẫn chăm sóc sau điều trị từ dữ liệu bệnh án. |
| **Actor / Operator** | Bác sĩ điều trị, điều dưỡng, nhân viên hồ sơ bệnh án. |
| **Quy trình hiện tại** | 1) Bác sĩ xem chẩn đoán, diễn biến và đơn thuốc. 2) Tự viết tóm tắt xuất viện. 3) Viết hướng dẫn tái khám/chăm sóc. 4) Kiểm tra, ký duyệt và bàn giao cho bệnh nhân. |
| **Bottleneck** | Tóm tắt thông tin từ nhiều trường trong bệnh án và diễn đạt dễ hiểu cho bệnh nhân mất khoảng 20–30 phút mỗi ca, đặc biệt vào thời điểm xuất viện cao điểm. |
| **AI Solution** | Tạo bản nháp theo mẫu cố định từ dữ liệu bệnh án được cấp quyền; kiểm tra thiếu trường thông tin và đưa bác sĩ màn hình so sánh nguồn trước khi ký. |
| **Metric thành công** | Giảm thời gian soạn thảo ít nhất 40%; 100% hồ sơ do bác sĩ duyệt trước khi phát hành; tỷ lệ thiếu trường bắt buộc dưới 1%. |
| **Rủi ro & boundary** | Dữ liệu y tế là nhạy cảm; AI không được chẩn đoán, tự thay đổi đơn thuốc hoặc phát hành tài liệu chưa có chữ ký bác sĩ. Cần đánh giá bảo mật, quyền truy cập và tuân thủ trước pilot. |
| **Đánh giá nhanh** | **Chưa ưu tiên pilot đầu tiên.** Giá trị cao nhưng rủi ro dữ liệu và yêu cầu kiểm định chuyên môn cao hơn đáng kể. |

---

## Quyết định của nhóm

Nhóm chọn **Quick Problem Card #1 — Vinhomes: Phân loại & điều hướng phản ánh cư dân** cho bước Deep-Dive.

**Lý do:** Bài toán có tần suất cao, quy trình hiện hữu rõ ràng, rủi ro có thể kiểm soát bằng rule-based router và human-in-the-loop, đồng thời tạo tác động trực tiếp đến thời gian phản hồi cư dân. Hai bài toán còn lại được giữ trong backlog: Xanh SM cần kiểm chứng tích hợp dữ liệu thời gian thực; Vinmec cần đánh giá kỹ hơn về dữ liệu nhạy cảm và an toàn lâm sàng.
