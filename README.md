# Hệ thống Ngày hội việc làm tích hợp AI (CSE3051 — sản phẩm tổng hợp Buổi 1–10)

Hệ thống một cổng cho Ngày hội việc làm: sinh viên đăng ký phiên, hỏi đáp quy chế (RAG có trích dẫn),
trò chuyện với trợ lý đăng ký (agent có cổng xác nhận); Phòng CTSV xem thống kê có định nghĩa,
chạy cộng điểm rèn luyện tự động và tạo poster đúng thông tin. Mô hình ngôn ngữ chạy cục bộ qua Ollama;
khi không có Ollama, hệ thống tự chuyển sang chế độ offline (không dùng LLM) và vẫn vận hành an toàn.

## Chạy nhanh (Windows: thay `source .venv/bin/activate` bằng `.venv\Scripts\activate`)
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q                       # 24 passed
cp .env.example .env                      # rồi sửa ADMIN_KEY
ADMIN_KEY=ctsv-2026 uvicorn app.main:app --reload
```
Mở http://localhost:8000 (giao diện) và http://localhost:8000/docs (tài liệu API).

### Lưu ý khi chạy trên Windows
Hai lỗi gặp khi chạy đúng các lệnh trên ở Windows 11 (Python 3.13), và cách xử lý không cần sửa mã:

| Hiện tượng | Nguyên nhân | Cách xử lý (PowerShell) |
|---|---|---|
| `UnicodeEncodeError` khi script in tiếng Việt | Cửa sổ lệnh dùng bảng mã cp1252 | `$env:PYTHONUTF8 = "1"` |
| `pytest` báo 23/24, `test_poster_tuong_phan_va_doi_chieu` lỗi `OSError: cannot open resource` | `app/poster.py` mặc định đọc phông DejaVu ở đường dẫn Linux `/usr/share/fonts/truetype/dejavu/` | Trỏ `FONT_PATH` và `FONT_BOLD_PATH` tới phông DejaVu đi kèm matplotlib (xem dưới) |

```
$ttf = ".venv\Lib\site-packages\matplotlib\mpl-data\fonts\ttf"
$env:FONT_PATH = (Resolve-Path "$ttf\DejaVuSans.ttf").Path
$env:FONT_BOLD_PATH = (Resolve-Path "$ttf\DejaVuSans-Bold.ttf").Path
$env:ADMIN_KEY = "ctsv-2026"; uvicorn app.main:app --reload
```
PowerShell không nhận cú pháp `BIEN=gia_tri lenh`; đặt biến bằng `$env:BIEN = "..."` trước khi chạy lệnh.

## Bật mô hình ngôn ngữ cục bộ
```
ollama pull qwen2.5:3b && ollama pull bge-m3
python scripts/nhung.py && python scripts/danh_gia_rag.py   # đo lại ngưỡng cho bge-m3
```

## Thành phần ↔ buổi học
| Thành phần | Tệp | Buổi |
|---|---|---|
| Gọi LLM cục bộ, temperature 0, câu lệnh 4 thành phần | app/llm.py, app/rag.py | 1 |
| Quy ước mã rõ nghĩa, kiểm thử do người viết | tests/, AGENTS.md | 2 |
| API, mã trạng thái, UNIQUE, CORS, giao diện | app/main.py, app/db.py, web/ | 3 |
| Đặc tả bảng ví dụ, test đỏ–xanh, chống vượt chỗ khi đồng thời | spec.md, app/dang_ky.py, scripts/ban_dong_thoi.py | 4 |
| CI, mẫu PR, quy tắc agent | .github/, AGENTS.md | 5 |
| RAG: cắt theo Điều, ngưỡng, câu hỏi vàng | app/rag.py, scripts/danh_gia_rag.py | 6 |
| Agent: phân quyền, cổng xác nhận, nhật ký, bộ nhiệm vụ | app/agent.py, scripts/danh_gia_agent.py | 7 |
| Hồ sơ dữ liệu, hợp đồng chỉ số, tập nhỏ, biểu đồ | app/phan_tich.py, docs/chi_so.md | 8 |
| Cộng điểm chạy lại an toàn, ngoại lệ, lịch | app/tu_dong.py, scripts/cong_diem.py | 9 |
| Poster: nền có seed, chữ đặt bằng mã, 3 phép kiểm | app/poster.py, data/poster/ | 10 |

Dữ liệu trong data/ là dữ liệu MÔ PHỎNG (sinh bằng scripts/sinh_du_lieu.py, SEED = 2026).
Triển khai thật: xem docs/trien_khai.md.
