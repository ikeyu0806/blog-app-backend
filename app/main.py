from typing import Optional
import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure import db

app = FastAPI()

origins = [
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create_post")
def create_post():
    dt = datetime.datetime.now()

    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO posts (title, content) VALUES (%s, %s, %s, %s)', ('title', 'content', dt, dt))
        conn.commit()
    return {"create_post": "create_post"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
