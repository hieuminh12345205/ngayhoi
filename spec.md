# Giới hạn chỗ mỗi phiên

Sức chứa: **30 sinh viên / phiên**. Đếm riêng từng phiên.
API: `POST /api/dang-ky`, JSON gồm `ma_sv`, `ma_phien`.

| # | Đang có | Hành động | Kết quả |
|---|---|---|---|
| 1 | P01 trống | SV001 đăng ký P01 | 201, `{"ok":true}` |
| 2 | P01 có 29 | SV mới đăng ký P01 | 201, P01 có đúng 30 |
| 3 | P01 có 30 | SV mới đăng ký P01 | 409, `{"detail":"HET_CHO"}`; số lượng vẫn 30 |
| 4 | P01 có 30, gồm SV000 | SV000 đăng ký lại P01 | 409, `{"detail":"DA_DANG_KY"}`; số lượng vẫn 30 |
| 5 | P01 có 30; P02 trống | SV031 đăng ký P02 | 201, P01 vẫn 30; P02 có 1 |
| 6 | Một phiên trống | 40 SV khác nhau gửi cùng lúc | Đúng 30 × 201, 10 × 409 HET_CHO; CSDL có đúng 30 |

Quy tắc ưu tiên: **kiểm tra đã đăng ký trước khi kiểm tra hết chỗ**.
Người dùng đã xác nhận giữ quy tắc dòng 4 như ảnh ngày 09/10/2026.
Yêu cầu đồng thời không được vượt sức chứa; kiểm tra và ghi phải cùng một
giao dịch giữ khóa ghi SQLite. Giữ UNIQUE(ma_sv, ma_phien) của Buổi 3.

Ngoài phạm vi: hủy đăng ký, danh sách chờ, xác thực tài khoản, thay đổi sức
chứa, thay đổi lịch phiên, sinh lại giao diện bằng v0.dev. Bài Buổi 4 tập trung
backend, kiểm thử và Git. Giao diện chỉ bổ sung phân biệt HET_CHO và DA_DANG_KY.
