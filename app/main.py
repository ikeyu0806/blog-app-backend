from pydantic import BaseModel
import datetime

from fastapi import FastAPI, Form
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

class Post(BaseModel):
    title: str
    content: str

@app.post("/create_post")
def create_post(post: Post):
    dt = datetime.datetime.now()

    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO posts (title, content, created_at, updated_at) VALUES (%s, %s, %s, %s)', (post.title, post.content, dt, dt))
        conn.commit()
    return {"post": post}
