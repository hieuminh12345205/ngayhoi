"""Kiểm tra dữ liệu thật trong SQLite tạm, không sửa ngayhoi.db."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import unittest
from fastapi.testclient import TestClient
import main


class RegistrationTests(unittest.TestCase):
    def test_registration_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            old_path = main.DB_PATH
            main.DB_PATH = Path(directory) / "test.db"
            try:
                with TestClient(main.app) as client:
                    payload = {"ma_sv": "23110198", "ma_phien": "P01"}
                    first = client.post("/api/dang-ky", json=payload)
                    self.assertEqual(first.status_code, 201)
                    self.assertEqual(first.json(), {"ok": True})
                    second = client.post("/api/dang-ky", json=payload)
                    self.assertEqual(second.status_code, 409)
                    self.assertEqual(second.json(), {"detail": "DA_DANG_KY"})
                    for bad in [{"ma_sv": "23110198"}, {"ma_sv": " ", "ma_phien": "P01"}, {"maSv": "23110198", "ma_phien": "P01"}]:
                        self.assertEqual(client.post("/api/dang-ky", json=bad).status_code, 422)
                    self.assertEqual(client.post("/api/dang-ky", json={**payload, "ma_phien": "P02"}).status_code, 201)
                    self.assertEqual(client.post("/api/dang-ky", json={**payload, "ma_sv": "OTHER"}).status_code, 201)
                    allowed = client.options("/api/dang-ky", headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "content-type"})
                    self.assertEqual(allowed.status_code, 200)
                    self.assertEqual(allowed.headers["access-control-allow-origin"], "http://localhost:5173")
                    rejected = client.options("/api/dang-ky", headers={"Origin": "http://example.com", "Access-Control-Request-Method": "POST"})
                    self.assertNotIn("access-control-allow-origin", rejected.headers)
                    with ThreadPoolExecutor(max_workers=6) as pool:
                        codes = list(pool.map(lambda _: client.post("/api/dang-ky", json={"ma_sv": "CONCURRENT", "ma_phien": "P01"}).status_code, range(6)))
                    self.assertEqual(sorted(codes), [201, 409, 409, 409, 409, 409])
                # Ràng buộc vẫn hiệu lực sau khi khởi động lại ứng dụng.
                with TestClient(main.app) as restarted:
                    self.assertEqual(restarted.post("/api/dang-ky", json=payload).status_code, 409)
            finally:
                main.DB_PATH = old_path


if __name__ == "__main__":
    unittest.main(verbosity=2)
