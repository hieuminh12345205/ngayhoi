# Bài thực hành Buổi 3 — Cổng đăng ký Ngày hội việc làm

Mã sinh viên: **23110198**. Bộ mã nguồn FastAPI + SQLite, React + Vite.

## Chạy ứng dụng

Cần Python 3.10+ và Node.js đáp ứng Vite 7 (20.19+ hoặc 22.12+).
Mở hai terminal tại thư mục `B3_23110198` đã giải nén.

Terminal 1 (backend):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
cd backend
..\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2 (frontend):

```powershell
cd frontend
npm install
npm run dev
```

Cũng có thể chạy hai script `start-backend.ps1` và `start-frontend.ps1` trong
hai terminal nếu máy cho phép chạy script PowerShell. Không cần tệp `.env`.

Mở giao diện tại **http://localhost:5173** và Swagger tại **http://localhost:8000/docs**.
Phải dùng `localhost:5173` vì CORS chỉ cho phép đúng origin này. Vite có
`--strictPort` để không tự đổi cổng. Frontend gọi thẳng FastAPI, không qua proxy.
Trên macOS/Linux tạo môi trường bằng `python3 -m venv .venv`, kích hoạt bằng
`source .venv/bin/activate`, sau đó dùng `python -m pip ...` và `python -m uvicorn ...`.

SQLite tự tạo `backend/ngayhoi.db` khi khởi động lần đầu. ZIP không kèm DB thử
nghiệm nên lần gửi đầu tiên trên máy mới sẽ trả 201. Dữ liệu được giữ qua lần
khởi động sau; cùng mã sinh viên và mã phiên sẽ tiếp tục trả 409.

## Thử API trên /docs

1. Mở POST `/api/dang-ky` → Try it out.
2. Nhập `{"ma_sv":"2220001","ma_phien":"P01"}` → Execute.
3. Lần đầu: **201**, body `{"ok":true}`.
4. Execute lần nữa với nguyên dữ liệu: **409**, body `{"detail":"DA_DANG_KY"}`.
5. Bỏ `ma_phien`: **422**, lỗi `Field required` do Pydantic.

Nếu dữ liệu đã tồn tại, dùng mã sinh viên mới để kiểm tra lần đầu. Không cần
xóa cơ sở dữ liệu. Ràng buộc `UNIQUE(ma_sv, ma_phien)` nằm trong SQLite;
không chỉ kiểm tra trùng trên giao diện. Câu SQL có tham số để tránh ghép dữ liệu
người dùng vào lệnh SQL. Trường thừa/sai tên, rỗng hay chỉ có khoảng trắng trả 422.

## Thử giao diện

Nhập mã sinh viên và chọn phiên. Ba trạng thái chính:

- Chưa gửi: thông tin “Mỗi phiên, một lượt đăng ký”.
- HTTP 201: “Đăng ký thành công”.
- HTTP 409: “Bạn đã đăng ký phiên này”.

Form giữ dữ liệu để dễ gửi lại. Đổi mã hoặc phiên sẽ đưa thông báo về trạng thái
chưa gửi. Có khóa nút trong lúc gửi, timeout 10 giây, thông báo riêng cho 422,
lỗi máy chủ hoặc lỗi mạng. Các phiên và thời gian hiển thị là dữ liệu minh họa
cho bài thực hành, không phải lịch sự kiện chính thức. API chấp nhận mã phiên
hợp lệ về định dạng để tương thích dữ liệu mẫu; chưa có bảng lịch phiên từ đề.

## Minh chứng và kiểm tra

Thư mục `evidence/` có ảnh chụp thật trên trình duyệt:

- `docs-01-201.jpg`, `docs-02-409.jpg`: cùng dữ liệu 2220001/P01, gửi liên tiếp.
- `docs-03-422.jpg`: thiếu trường ma_phien.
- `ui-01-chua-gui.jpg`, `ui-02-thanh-cong.jpg`, `ui-03-da-dang-ky.jpg`:
  ba trạng thái; hai lần gửi giao diện dùng 23110198/P01.

Các ảnh được chụp khi chạy API thật với cơ sở dữ liệu minh chứng riêng, không
đưa dữ liệu đó vào bài nộp. Xem `so-do.md` và `so-do.svg` cho luồng xử lý.

Chạy kiểm tra backend (dùng SQLite tạm, không tác động dữ liệu ứng dụng):

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements-test.txt
cd backend
..\.venv\Scripts\python.exe -m unittest -v test_api
```

Build frontend: `cd frontend` rồi `npm run build`. Đã kiểm tra build Vite và
API 201/409/422, CORS cho phép/từ chối origin, nhiều yêu cầu đồng thời và đăng
ký trùng sau khi khởi động lại. Có CSS responsive; kiểm tra viewport điện thoại
chưa được xác nhận do công cụ trình duyệt không áp dụng kích thước yêu cầu.

## Đối chiếu yêu cầu từ slide

| Yêu cầu | Sản phẩm |
|---|---|
| main.py chạy được | backend/main.py, requirements.txt |
| /docs lần 1 201, lần 2 409 | Hai ảnh docs trong evidence/ |
| Ba trạng thái giao diện | Ba ảnh ui trong evidence/ |
| CORS đúng một địa chỉ | allow_origins=["http://localhost:5173"] |
| Sơ đồ | so-do.md và so-do.svg |
| B3_{MaSV}.zip, không .venv/node_modules | B3_23110198.zip |
| Giao diện sinh từ v0.dev | **Chưa thực hiện trên v0.dev**; có prompt-v0.md |

Mã mẫu Buổi 2 chưa được cung cấp nên backend được viết mới theo hợp đồng API
trong ảnh. Giao diện hiện được tự xây dựng bởi Codex, chưa có bản xuất từ v0.dev.
Nếu giảng viên bắt buộc dùng v0.dev, cần chạy prompt trong `prompt-v0.md`, lưu
bản xuất/ảnh và đối chiếu trước khi nộp. Không coi prompt là bằng chứng sử dụng v0.
Bài chưa được gửi lên MS Teams; sinh viên kiểm tra và nộp ZIP trước Buổi 4.

Tài liệu tham khảo: [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/),
[Vite Getting Started](https://vite.dev/guide/).
