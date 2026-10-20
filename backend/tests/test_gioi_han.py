import os

# Phải đặt trước import main. Không sử dụng ngayhoi.db thật.
os.environ["DB_PATH"] = ":memory:"

import pytest
from fastapi.testclient import TestClient
import main


@pytest.fixture(autouse=True)
def client():
    with TestClient(main.app) as test_client:
        with main.connect() as db:
            db.execute("DELETE FROM dang_ky")
        yield test_client


def lap_day(client, ma_phien, n):
    for i in range(n):
        response = client.post(
            "/api/dang-ky", json={"ma_sv": f"SV{i:03}", "ma_phien": ma_phien}
        )
        assert response.status_code == 201


def so_luong(ma_phien):
    with main.connect() as db:
        return db.execute(
            "SELECT COUNT(*) FROM dang_ky WHERE ma_phien = ?", (ma_phien,)
        ).fetchone()[0]


def test_phien_trong_nhan_sinh_vien_dau_tien(client):
    response = client.post("/api/dang-ky", json={"ma_sv": "SV001", "ma_phien": "P01"})
    assert response.status_code == 201
    assert response.json() == {"ok": True}
    assert so_luong("P01") == 1


def test_29_cho_nhan_nguoi_thu_30(client):
    lap_day(client, "P01", 29)
    response = client.post("/api/dang-ky", json={"ma_sv": "SV030", "ma_phien": "P01"})
    assert response.status_code == 201
    assert response.json() == {"ok": True}
    assert so_luong("P01") == 30


def test_nguoi_thu_31_bi_tu_choi(client):
    lap_day(client, "P01", 30)
    response = client.post("/api/dang-ky", json={"ma_sv": "SV031", "ma_phien": "P01"})
    assert response.status_code == 409
    assert response.json() == {"detail": "HET_CHO"}
    assert so_luong("P01") == 30


def test_phien_day_van_uu_tien_da_dang_ky(client):
    lap_day(client, "P01", 30)
    response = client.post("/api/dang-ky", json={"ma_sv": "SV000", "ma_phien": "P01"})
    assert response.status_code == 409
    assert response.json() == {"detail": "DA_DANG_KY"}
    assert so_luong("P01") == 30


def test_phien_khac_van_con_cho(client):
    lap_day(client, "P01", 30)
    response = client.post("/api/dang-ky", json={"ma_sv": "SV031", "ma_phien": "P02"})
    assert response.status_code == 201
    assert response.json() == {"ok": True}
    assert so_luong("P01") == 30
    assert so_luong("P02") == 1
