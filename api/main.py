"""Reference API: FastAPI + PostgreSQL.

The full answer key for the Part 4 integration checkpoint.
Reads/writes the items table and exposes it as JSON. Talks to Postgres using
the DATABASE_URL set by Docker Compose.
"""
import os
import time

import psycopg
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DATABASE_URL = os.environ["DATABASE_URL"]
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")

app = FastAPI(title="Reference Items API")

# let the Next.js frontend (another origin) call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ItemIn(BaseModel):
    name: str
    price: float = Field(gt=0)


class Item(ItemIn):
    id: int


def _connect() -> psycopg.Connection:
    """Connect to Postgres, retrying briefly while the DB finishes starting."""
    last_error: Exception | None = None
    for _ in range(10):
        try:
            return psycopg.connect(DATABASE_URL)
        except psycopg.OperationalError as err:   # DB not ready yet
            last_error = err
            time.sleep(1)
    raise RuntimeError(f"could not connect to database: {last_error}")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/items")
def list_items() -> list[Item]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, name, price FROM items ORDER BY id"
        ).fetchall()
    return [Item(id=r[0], name=r[1], price=float(r[2])) for r in rows]


@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, name, price FROM items WHERE id = %s", (item_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(id=row[0], name=row[1], price=float(row[2]))


@app.post("/items", status_code=201)
def create_item(payload: ItemIn) -> Item:
    with _connect() as conn:
        row = conn.execute(
            "INSERT INTO items (name, price) VALUES (%s, %s) RETURNING id",
            (payload.name, payload.price),
        ).fetchone()
        conn.commit()
    return Item(id=row[0], **payload.model_dump())
