"""Cổng đăng ký Ngày hội việc làm — FastAPI + SQLite."""
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from typing import Annotated
import os
import sqlite3

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

DB_PATH = os.getenv("DB_PATH", os.getenv("NGAYHOI_DB", str(Path(__file__).with_name("ngayhoi.db"))))
MEMORY_URI = "file:ngayhoi-test?mode=memory&cache=shared"
SUC_CHUA = 30


@contextmanager
def connect():
    # Giữ CSDL :memory: chung cho các kết nối trong một lượt TestClient.
    memory = str(DB_PATH) == ":memory:"
    db = sqlite3.connect(MEMORY_URI if memory else DB_PATH, uri=memory, timeout=10)
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
    keeper = sqlite3.connect(MEMORY_URI, uri=True) if str(DB_PATH) == ":memory:" else None
    try:
        init_db()
        yield
    finally:
        if keeper is not None:
            keeper.close()


app = FastAPI(title="Ngày hội việc làm", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


class DangKy(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    ma_sv: str = Field(min_length=1, max_length=30, pattern=r"^[A-Za-z0-9_-]+$")
    ma_phien: str = Field(min_length=1, max_length=30, pattern=r"^[A-Za-z0-9_-]+$")


class KetQua(BaseModel):
    ok: bool


@app.get("/api/con-cho", summary="Số chỗ còn lại của một phiên")
def con_cho(
    ma_phien: Annotated[
        str, Query(min_length=1, max_length=30, pattern=r"^[A-Za-z0-9_-]+$")
    ],
) -> dict[str, int]:
    with connect() as db:
        count = db.execute(
            "SELECT COUNT(*) FROM dang_ky WHERE ma_phien = ?", (ma_phien,)
        ).fetchone()[0]
    return {"con_cho": max(0, SUC_CHUA - count)}


@app.post(
    "/api/dang-ky",
    status_code=status.HTTP_201_CREATED,
    response_model=KetQua,
    summary="Đăng ký một phiên",
    responses={409: {"description": "DA_DANG_KY (ưu tiên) hoặc HET_CHO khi phiên đủ 30"}},
)
def dang_ky(data: DangKy):
    try:
        with connect() as db:
            # Giữ khóa ghi trước SELECT: kiểm tra và INSERT cùng một giao dịch.
            db.execute("BEGIN IMMEDIATE")
            existed = db.execute(
                "SELECT 1 FROM dang_ky WHERE ma_sv = ? AND ma_phien = ?",
                (data.ma_sv, data.ma_phien),
            ).fetchone()
            if existed:
                raise HTTPException(status_code=409, detail="DA_DANG_KY")
            count = db.execute(
                "SELECT COUNT(*) FROM dang_ky WHERE ma_phien = ?", (data.ma_phien,)
            ).fetchone()[0]
            if count >= SUC_CHUA:
                raise HTTPException(status_code=409, detail="HET_CHO")
            db.execute(
                "INSERT INTO dang_ky (ma_sv, ma_phien) VALUES (?, ?)",
                (data.ma_sv, data.ma_phien),
            )
    except sqlite3.IntegrityError as exc:
        if "UNIQUE constraint failed" in str(exc):
            raise HTTPException(status_code=409, detail="DA_DANG_KY") from exc
        raise
    return {"ok": True}
