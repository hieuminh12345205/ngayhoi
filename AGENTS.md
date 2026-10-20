# Quy tắc làm việc trong kho

## Dự án và hợp đồng

- FastAPI + SQLite ở `backend/`; React + Vite ở `frontend/`.
- POST `/api/dang-ky`: 201 khi ghi thành công; 409 `DA_DANG_KY` trước `HET_CHO`.
- Giữ sức chứa 30, UNIQUE(ma_sv, ma_phien), SQL tham số và BEGIN IMMEDIATE.

## Phạm vi PR con-cho

- Chỉ sửa `backend/main.py`, thêm `backend/tests/test_con_cho.py` và tệp quy tắc này.
- Không sửa `backend/tests/test_gioi_han.py`, `.github/`, frontend hoặc dependency.
- Không thay đổi nghiệp vụ POST để làm test GET đạt.
- GET `/api/con-cho?ma_phien=P01` trả `{"con_cho": n}`.
- Đếm riêng phiên; số chỗ là max(0, 30 - số đăng ký). Phiên trống còn 30.
- Mã phiên bắt buộc, 1–30 ký tự ASCII chữ/số/`_`/`-`; sai trả 422.
- GET chỉ đọc, không giữ chỗ và không tạo đăng ký. Không thêm giao diện.

## Test và bằng chứng

- Viết test mới trước, chạy đỏ rồi mới triển khai. Giữ log và commit đúng thứ tự.
- Dùng SQLite tạm/bộ nhớ, không đọc/ghi DB thật từ test.
- Chạy tại `backend/`: `python -m pytest -q` và `python -m unittest -v test_api`.
- Không sửa, xóa hoặc skip test cũ để làm xanh. Không ghi kiểm tra chưa chạy là PASS.
- Không đưa token, DB, .venv, node_modules hoặc dữ liệu người dùng vào Git.

## PR và duyệt

- Diff PR tính tổng dòng thêm/xóa phải dưới 200; tách việc nếu vượt phạm vi.
- Mô tả có Việc, Vì sao, Bằng chứng, Phần AI làm, Cần soi kỹ.
- Ghi đúng phần AI hỗ trợ. Nhận xét AI không thay lượt Approve của người khác.
- Chỉ merge khi CI xanh và đủ duyệt; giữ luật bảo vệ, không bypass để hoàn tất bài.
