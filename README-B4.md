# Buổi 4 — Giới hạn 30 chỗ mỗi phiên

Mã sinh viên: **23110198**. Tiếp tục mã Buổi 3. Nhánh Git: `gioi-han-cho`.

## Sản phẩm chính

- `spec.md`: sáu ví dụ, ưu tiên DA_DANG_KY được người dùng xác nhận.
- `backend/tests/test_gioi_han.py`: đúng năm test pytest + TestClient theo dòng 1–5.
- `backend/main.py`: giới hạn 30, UNIQUE, giao dịch BEGIN IMMEDIATE.
- `backend/ban_dong_thoi.py`: 40 yêu cầu HTTP thật, có Barrier đồng bộ bắt đầu.
- Giao diện phân biệt `HET_CHO` (“Phiên đã hết chỗ”) và `DA_DANG_KY`.
- `evidence-b4/`: stdout nguyên văn, JSON từng yêu cầu, ảnh báo cáo và lịch sử Git.
- `ngayhoi.bundle`: toàn bộ lịch sử Git để phục hồi repository.

## Chạy trên máy của bạn

Cần Python **3.11+**, Git. Tại thư mục bài đã giải nén:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements-test.txt
cd backend
..\.venv\Scripts\python.exe -m pytest -q
```

Kết quả mong đợi: **5 passed**. SQLite dùng chung trong bộ nhớ, tạo và giữ một
kết nối neo trong vòng đời TestClient, đóng khi kết thúc. Đặt `DB_PATH=:memory:`
trước khi import main; fixture dọn bảng trước mỗi test. Không đụng DB thật.
Không dùng cùng một kết nối SQLite không bảo vệ giữa các luồng.

Terminal 1, tại `backend/`:

```powershell
..\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2, tại `backend/`:

```powershell
..\.venv\Scripts\python.exe ban_dong_thoi.py P20 --db ngayhoi.db --expect-limit
```

Mỗi lần chạy dùng **một mã phiên mới**: P20, P21... DB phải là DB của máy chủ.
Nếu máy chủ sử dụng `DB_PATH` khác, truyền đường dẫn đó vào `--db`.
Kết quả phải là **201: 30 · 409: 10**, và CSDL có đúng 30 hàng của phiên đó.
Mười phản hồi 409 đều có body `{"detail":"HET_CHO"}`.
Script từ chối phiên có dữ liệu sẵn khi dùng `--db`, không xóa dữ liệu.

Trên macOS/Linux, dùng `python3 -m venv .venv`, `source .venv/bin/activate`,
sau đó thay đường dẫn Python Windows bằng `python`.
Giao diện/API `/docs` và cách cài frontend xem `README.md` của Buổi 3.

## Bốn cổng và bằng chứng thực tế

1. **Git và đặc tả:** commit mã Buổi 3, tạo nhánh `gioi-han-cho`, viết sáu ví dụ.
2. **Test đỏ:** `1 failed, 4 passed`, đúng test người thứ 31 với `assert 201 == 409`.
   Commit đặc tả và test trước khi thêm giới hạn. Từ đây không sửa `backend/tests/`.
3. **Mã xanh:** thêm kiểm tra trùng rồi đếm chỗ; năm test đạt tuần tự.
4. **Đồng thời và soát:** bản chưa khóa có `sleep(0.05)` trước INSERT để mở rộng
   khe hở; 40 HTTP trên P09 → **40 × 201, 0 × 409**, DB có 40.
   Thêm `db.execute("BEGIN IMMEDIATE")` trước SELECT rồi bỏ sleep;
   40 HTTP trên P10 → **30 × 201, 10 × 409**, DB có 30.
   Năm test vẫn đạt. Kiểm tra hồi quy Buổi 3 (201/409/422, CORS, UNIQUE) cũng đạt.

BEGIN IMMEDIATE lấy quyền ghi trước khi đọc số lượng, để các yêu cầu khác chờ
giao dịch hiện tại commit/rollback. Vì kiểm tra trùng, đếm và INSERT nằm cùng
giao dịch nên hai yêu cầu không cùng lấy chỗ thứ 30.
Tham khảo: [SQLite Transaction](https://www.sqlite.org/lang_transaction.html).
Không dùng khóa Python chỉ có tác dụng trong một tiến trình.

Ảnh trong `evidence-b4/` là ảnh trình duyệt hiển thị **stdout được lưu từ lệnh
chạy thật**, có ghi rõ nguồn; không dựng giả ảnh terminal hay kết quả kiểm thử.
Các tệp `.txt` và `.json` là nguồn đối chiếu. Có cảnh báo deprecation của
Starlette về httpx; đây không phải test failure và không bị bỏ khỏi stdout.
DB thí nghiệm nằm ngoài gói, không chuyển 40 đăng ký của bản lỗi sang bài nộp.

`main-truoc-khoa.py.txt` và `truoc-khoa.patch` ghi lại bản thí nghiệm trước khi
sửa, chỉ là bằng chứng; mã đang chạy là `backend/main.py` đã bỏ sleep.
Giới hạn này ngăn đăng ký mới vượt 30; không tự xóa dữ liệu cũ nếu phiên đã
vượt 30 từ bản trước. Bài nộp không kèm `.db`, `.venv`, `node_modules`.

## Lịch sử Git và tính bất biến của test

Có ba commit tổng cộng: **một commit nền Buổi 3 và hai commit Buổi 4** (test đỏ,
triển khai cuối). Commit Buổi 4 có ghi nhận Codex hỗ trợ sinh mã/test, nguồn
đặc tả do người dùng xác nhận và các kết quả đã chạy thật.

Repository đang làm việc có `.git` tại thư mục bài. ZIP không kèm `.git`; thay
vào đó có `ngayhoi.bundle` giữ toàn bộ lịch sử và hai nhánh. Để phục hồi sau khi
giải nén, tại thư mục bài:

```powershell
git init
git fetch ngayhoi.bundle refs/heads/main:refs/heads/main refs/heads/gioi-han-cho:refs/heads/gioi-han-cho
git symbolic-ref HEAD refs/heads/gioi-han-cho
git reset --mixed HEAD
git log --oneline --decorate
```

Các lệnh trên giữ nguyên tệp làm việc, phục hồi index từ commit; không dùng
`--hard`. `ngayhoi.bundle`/`evidence-b4` được gitignore. Xem
`evidence-b4/git-log.txt` và `audit.json` cho hash commit, SHA-256 test và bằng
chứng không thay đổi `backend/tests/` từ commit test đỏ đến mã cuối.

Trong các ảnh được cung cấp chỉ có hướng dẫn chi tiết bước 1–6; bước 7–8 được
thực hiện theo phần tổng quan: khóa giao dịch, soát diff và commit ghi nhận AI.
Bài chưa được tải lên MS Teams. V0.dev vẫn là mục chưa thực hiện từ Buổi 3,
đã ghi trong `README.md` và không được nhận là hoàn tất trong bài Buổi 4.
