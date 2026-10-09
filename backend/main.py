"""Cổng đăng ký Ngày hội việc làm — FastAPI + SQLite."""
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
import os
import sqlite3

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

DB_PATH = Path(os.environ.get("NGAYHOI_DB", Path(__file__).with_name("ngayhoi.db")))


@contextmanager
def connect():
    db = sqlite3.connect(DB_PATH, timeout=10)
    try:
        with db:
            yield db
    finally:
        db.close()


def init_db():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS dang_ky (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ma_sv TEXT NOT NULL,
                ma_phien TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(ma_sv, ma_phien)
            )
        """)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Ngày hội việc làm", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class DangKy(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    ma_sv: str = Field(min_length=1, max_length=30, pattern=r"^[A-Za-z0-9_-]+$")
    ma_phien: str = Field(min_length=1, max_length=30, pattern=r"^[A-Za-z0-9_-]+$")


class KetQua(BaseModel):
    ok: bool


@app.post(
    "/api/dang-ky",
    status_code=status.HTTP_201_CREATED,
    response_model=KetQua,
    summary="Đăng ký một phiên",
    responses={409: {"description": "Đã đăng ký cùng mã sinh viên và mã phiên"}},
)
def dang_ky(data: DangKy):
    try:
        with connect() as db:
            db.execute(
                "INSERT INTO dang_ky (ma_sv, ma_phien) VALUES (?, ?)",
                (data.ma_sv, data.ma_phien),
            )
    except sqlite3.IntegrityError as exc:
        if "UNIQUE constraint failed" in str(exc):
            raise HTTPException(status_code=409, detail="DA_DANG_KY") from exc
        raise
    return {"ok": True}
