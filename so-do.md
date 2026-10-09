# Sơ đồ cổng đăng ký Ngày hội việc làm

Mã sinh viên: 23110198. Bài thực hành CSE3051 — Buổi 3.

```mermaid
flowchart TD
  UI[React / Vite: localhost:5173] -->|Nhập ma_sv, chọn ma_phien| FORM[Nhấn Đăng ký]
  FORM -->|fetch POST JSON| CORS[FastAPI: localhost:8000 / api / dang-ky]
  CORS -->|Origin được phép| VALID[Pydantic kiểm tra DangKy]
  CORS -->|Origin khác| BLOCK[Trình duyệt chặn đọc phản hồi]
  VALID -->|Thiếu trường / sai dữ liệu| E422[422: thông báo kiểm tra dữ liệu]
  VALID -->|Hợp lệ| SQL[INSERT INTO dang_ky]
  SQL --> DB[(SQLite: UNIQUE ma_sv, ma_phien)]
  DB -->|Ghi thành công| R201[201: ok = true]
  DB -->|Vi phạm UNIQUE| R409[409: DA_DANG_KY]
  R201 --> SUCCESS[Giao diện: Đăng ký thành công]
  R409 --> DUP[Giao diện: Bạn đã đăng ký phiên này]
```

Giao diện khởi đầu ở trạng thái chưa gửi. Trong lúc gửi, khóa form/nút và hiển
thị đang gửi. Khi nhận HTTP 201 hoặc 409, hiện thông báo tương ứng và giữ dữ liệu
để có thể gửi lại. Thay đổi dữ liệu đưa form về trạng thái chưa gửi. Lỗi 422,
lỗi máy chủ, lỗi mạng hay timeout có thông báo riêng.

CORS là kiểm soát origin của trình duyệt, không phải cơ chế xác thực. Ràng buộc
UNIQUE của SQLite đảm bảo một cặp mã chỉ được ghi một lần ngay cả khi nhiều
yêu cầu đến đồng thời. Khởi động lại không làm mất dữ liệu đăng ký.

Ảnh sơ đồ độc lập: [so-do.svg](so-do.svg).
