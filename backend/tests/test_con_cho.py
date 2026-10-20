import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch, tmp_path):
    import main

    monkeypatch.setattr(main, "DB_PATH", tmp_path / "con-cho.db")
    with TestClient(main.app) as test_client:
        yield test_client


def seed(ma_phien, n):
    import main

    with main.connect() as db:
        db.executemany(
            "INSERT INTO dang_ky (ma_sv, ma_phien) VALUES (?, ?)",
            [(f"SV{i:03}", ma_phien) for i in range(n)],
        )


@pytest.mark.parametrize("occupancy, remaining", [(0, 30), (29, 1), (30, 0), (31, 0)])
def test_con_cho_theo_so_dang_ky(client, occupancy, remaining):
    # 31 mo phong du lieu cu vuot suc chua, GET khong tra so am.
    seed("P01", occupancy)
    response = client.get("/api/con-cho", params={"ma_phien": "P01"})
    assert response.status_code == 200
    assert response.json() == {"con_cho": remaining}


def test_dem_rieng_tung_phien_va_khong_sua_du_lieu(client):
    import main

    seed("P01", 30)
    seed("P02", 1)
    with main.connect() as db:
        before = db.execute("SELECT * FROM dang_ky ORDER BY id").fetchall()
    for ma_phien, remaining in [("P01", 0), ("P02", 29), ("P03", 30), ("P02", 29)]:
        response = client.get("/api/con-cho", params={"ma_phien": ma_phien})
        assert response.status_code == 200
        assert response.json() == {"con_cho": remaining}
    with main.connect() as db:
        assert db.execute("SELECT * FROM dang_ky ORDER BY id").fetchall() == before


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"ma_phien": ""},
        {"ma_phien": " "},
        {"ma_phien": " P01 "},
        {"ma_phien": "P 01"},
        {"ma_phien": "P/01"},
        {"ma_phien": "P" * 31},
    ],
)
def test_tu_choi_thieu_hoac_sai_ma_phien(client, params):
    response = client.get("/api/con-cho", params=params)
    assert response.status_code == 422
