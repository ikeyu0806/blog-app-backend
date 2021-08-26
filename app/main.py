from pydantic import BaseModel
import datetime
import json

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

class User(BaseModel):
    name: str
    email: str
    password: str

@app.post("/create_post")
def create_post(post: Post):
    dt = datetime.datetime.now()

    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO posts (title, content, created_at, updated_at) VALUES (%s, %s, %s, %s)', (post.title, post.content, dt, dt))
        conn.commit()
    return {"post": post}

@app.get("/posts")
def posts():
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM POSTS')
            result = cur.fetchall()
            
    key = ["id", "title", "content"]
    result = [dict(zip(key, post)) for post in result]
    print(result)

    return {'posts': result }

@app.post("/create_user")
def create_user(user: User):
    dt = datetime.datetime.now()

    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO users (name, email, encrypted_password, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)', (user.name, user.email, user.password, dt, dt))
        conn.commit()
    return {"user": user}
