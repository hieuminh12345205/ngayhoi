# Buổi 5 — GitHub, CI và pull request

Mã sinh viên: **23110198**. Tiếp tục lịch sử Buổi 4, giữ nguyên năm test giới hạn chỗ.

## Kho và nhánh

Kho dự kiến: `https://github.com/hieuminh12345205/ngayhoi`, chế độ **Private**.
`master` được phục hồi từ nhánh `main` của Buổi 3; `gioi-han-cho` chứa hai commit
Buổi 4 và bổ sung CI Buổi 5. Không viết lại ba commit gốc.

PR đầu tiên: `gioi-han-cho` → `master`. Mẫu PR có năm mục: Việc, Vì sao,
Bằng chứng, Phần AI làm, Cần soi kỹ. Người khác đọc diff và duyệt trước khi merge.

## CI

`.github/workflows/test.yml` chạy trên mọi pull request, khi push hai nhánh
chính và khi chạy thủ công. Workflow `test`, job `pytest`, Python 3.13:

```powershell
python -m pip install -r backend/requirements-test.txt
cd backend
python -m pytest -q
python -m unittest -v test_api
```

`working-directory: backend` giúp `import main` đúng. Pytest tìm trong `tests/`;
bộ unittest hồi quy Buổi 3 được chạy riêng. Các test dùng SQLite tạm/bộ nhớ,
không dùng cơ sở dữ liệu của ứng dụng.

## Bảo vệ master và thử cổng

Thiết lập trên GitHub, sau khi check đã chạy:

- Bắt buộc pull request và một lượt Approve từ người khác.
- Bắt buộc check `pytest` của GitHub Actions, hiển thị dưới workflow `test`.
- Nhánh phải cập nhật với `master`; áp dụng cả quản trị viên.
- Không cho force push hoặc xóa nhánh.

Giữ `SUC_CHUA = 30` ở backend. Trên nhánh PR đầu tiên, đổi tạm thành 31,
commit và push. Đợi CI đỏ, chụp trực tiếp PR cho thấy test đỏ và merge bị khóa.
Sau khi lưu ảnh, **revert commit thử lỗi**, push, đợi CI xanh. Không sửa test,
không bỏ luật bảo vệ để merge. Commit lỗi và commit revert được giữ trong lịch sử.

## PR nhỏ cho agent

Sau khi PR đầu được người khác duyệt và hợp nhất, từ `master` mới nhất tạo nhánh
`con-cho`. Đọc `AGENTS.md`, viết test mới trước rồi bổ sung:

```http
GET /api/con-cho?ma_phien=P01
200 {"con_cho": 30}
```

Số chỗ là `max(0, SUC_CHUA - số đăng ký của phiên)`. Phiên hợp lệ chưa có dữ liệu
còn 30 chỗ vì ứng dụng chưa có bảng danh mục phiên. GET không giữ chỗ; POST
vẫn là nơi quyết định nhận đăng ký bằng giao dịch. Tham số phải có và theo định
dạng mã hiện tại. Đây là các quy ước bổ sung vì ảnh không quy định hết biên dữ liệu.

PR agent chỉ thêm `AGENTS.md`, sửa backend và thêm test mới; dưới 200 dòng
thêm/xóa. Không sửa `backend/tests/test_gioi_han.py`, `.github/` hoặc frontend.

## Người duyệt và minh chứng

Cần tài khoản bạn cùng cặp/giảng viên được mời vào kho. Không tự Approve PR
của mình hoặc dùng nhận xét của AI thay cho lượt duyệt của người khác.
Người duyệt để lại ít nhất một góp ý theo dòng, Approve, rồi người viết merge
khi CI xanh. Chưa có tài khoản người duyệt thì PR phải tiếp tục chờ.

Checklist soát dưới đây do người triển khai bổ sung; không phải nguyên văn
năm câu hỏi Buổi 4 vì các ảnh không chứa phần đó:

1. Thay đổi có đúng đặc tả và nằm trong phạm vi PR không?
2. Kiểm tra trùng, hết chỗ và số chỗ theo phiên có đúng không?
3. Giao dịch, UNIQUE và truy vấn tham số có được giữ không?
4. Test có chứng minh hành vi và không sửa test cũ để che lỗi không?
5. CI, bằng chứng, mô tả PR và ghi nhận AI có khớp mã đang duyệt không?

Sản phẩm cần nộp: link kho và mời giảng viên; ảnh CI đỏ + merge bị khóa;
ảnh PR đầu đã merge; PR agent dưới 200 dòng, có test và CI.
Trạng thái thực tế và bằng chứng được lưu riêng ở `evidence-b5/` sau mỗi bước.
Chỉ ảnh chụp GitHub thật mới được coi là bằng chứng merge bị khóa/đã merge.

Ảnh cung cấp thiếu slide YAML 13 dòng, chi tiết bước 4, mẫu AGENTS và nguyên văn
năm câu hỏi review. Cấu hình/checklist ở đây là phần bổ sung theo yêu cầu quan sát
được; không tuyên bố chép nguyên văn các slide thiếu. Phần v0.dev từ Buổi 3 và
việc nộp MS Teams vẫn do người học hoàn tất.

Tham khảo chính thức:
[Python CI](https://docs.github.com/en/actions/tutorials/build-and-test-code/python),
[Bảo vệ nhánh](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).
