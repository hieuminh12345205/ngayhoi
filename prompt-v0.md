# Prompt để thực hiện bước v0.dev

Ghi chú nguồn gốc: giao diện React trong bài hiện được tự xây dựng bởi Codex;
chưa có bản xuất hay ảnh lịch sử tạo giao diện từ v0.dev. Prompt này chưa phải
bằng chứng đã sử dụng v0.dev. Nếu giảng viên bắt buộc quy trình này, nhập prompt
dưới đây vào v0.dev, lưu bản xuất/ảnh tạo giao diện và đối chiếu trước khi nộp.

---

Tạo giao diện tiếng Việt cho cổng đăng ký Ngày hội việc làm, dùng React và CSS,
chạy được trong Vite. Phong cách sáng, xanh lá trầm, trắng ngà, có điểm nhấn xanh
lime. Thiết kế responsive, nhãn form rõ ràng, điều khiển bằng bàn phím.

Hiển thị ba phiên minh họa P01, P02, P03. Form có mã sinh viên ma_sv (bắt buộc)
và mã phiên ma_phien (bắt buộc). Khi nhấn Đăng ký tham gia, dùng fetch POST đến
http://localhost:8000/api/dang-ky, Content-Type application/json, body chính xác
{"ma_sv":"23110198","ma_phien":"P01"} theo giá trị người dùng nhập/chọn.

Ba trạng thái chính: chưa gửi, thành công khi HTTP 201, đã đăng ký khi HTTP 409.
Thêm trạng thái đang gửi (khóa nút để tránh nhấp liên tiếp), lỗi 422, lỗi mạng.
Thông báo trùng phải là “Bạn đã đăng ký phiên này”, không coi 409 là thành công.
Thông báo có aria-live. Giữ dữ liệu sau khi gửi để dễ gửi lại cùng dữ liệu và
kiểm tra 409. Đừng mock kết quả; luôn gọi API thật. Không thêm backend hoặc
Next.js. Cung cấp toàn bộ mã để chép vào dự án React/Vite.
