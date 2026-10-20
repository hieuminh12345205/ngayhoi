"""Gửi 40 yêu cầu HTTP thật, mỗi lần chạy dùng một phiên mới."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sqlite3
from threading import Barrier

import httpx


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phien", help="Ví dụ P09, P10; chọn phiên chưa có đăng ký")
    parser.add_argument("--url", default="http://localhost:8000/api/dang-ky")
    parser.add_argument("--db", type=Path, help="Đường dẫn DB của máy chủ để kiểm tra số hàng")
    parser.add_argument("--json", type=Path, dest="output", help="Lưu kết quả chi tiết")
    parser.add_argument("--expect-limit", action="store_true", help="Yêu cầu đúng 30/10; sai thì exit 1")
    args = parser.parse_args()
    if args.db is not None:
        # mode=ro: không tự tạo DB khi người chạy gõ nhầm đường dẫn.
        with sqlite3.connect(args.db.resolve().as_uri() + "?mode=ro", uri=True) as db:
            before = db.execute("SELECT COUNT(*) FROM dang_ky WHERE ma_phien = ?", (args.phien,)).fetchone()[0]
        if before:
            parser.error(f"Phiên {args.phien} đã có {before} đăng ký. Hãy dùng phiên mới.")
    barrier = Barrier(40)
    with httpx.Client(timeout=30, trust_env=False, limits=httpx.Limits(max_connections=40, max_keepalive_connections=40)) as client:
        def gui(i):
            ma_sv = f"TN{i:03}"
            barrier.wait(timeout=30)
            response = client.post(args.url, json={"ma_sv": ma_sv, "ma_phien": args.phien})
            return {"ma_sv": ma_sv, "status": response.status_code, "body": response.json()}

        with ThreadPoolExecutor(max_workers=40) as executor:
            results = list(executor.map(gui, range(40)))
    codes = Counter(item["status"] for item in results)
    print(f"{args.phien} | 201: {codes[201]} · 409: {codes[409]} | Tổng: {len(results)}")
    summary = {"phien": args.phien, "url": args.url, "status_counts": dict(codes), "results": results}
    if args.db is not None:
        with sqlite3.connect(args.db.resolve().as_uri() + "?mode=ro", uri=True) as db:
            count = db.execute("SELECT COUNT(*) FROM dang_ky WHERE ma_phien = ?", (args.phien,)).fetchone()[0]
        summary["db_count"] = count
        print(f"CSDL {args.phien}: {count} đăng ký")
    valid = codes[201] == 30 and codes[409] == 10 and all(
        item["body"] == ({"ok": True} if item["status"] == 201 else {"detail": "HET_CHO"})
        for item in results
    ) and summary.get("db_count", 30) == 30
    summary["limit_ok"] = valid
    if args.output is not None:
        args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.expect_limit and not valid:
        raise SystemExit("FAIL: kết quả không đúng 30 × 201 / 10 × 409 HET_CHO")
    print("PASS: đúng giới hạn 30 chỗ" if valid else "KHÔNG ĐẠT giới hạn: xem mã HTTP và số hàng CSDL ở trên")


if __name__ == "__main__":
    run()
