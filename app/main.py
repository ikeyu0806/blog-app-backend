from pydantic import BaseModel
import datetime
import json
import hashlib
import traceback
import base64

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

class createUser(BaseModel):
    name: str
    email: str
    password: str

class loginUser(BaseModel):
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

    return {post: post }

@app.post("/create_user")
def create_user(user: createUser):
    dt = datetime.datetime.now()
    encrypted_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()

    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO users (name, email, encrypted_password, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)', (user.name, user.email, encrypted_password, dt, dt))
        conn.commit()
    # sessionIdは本当はもう少し凝ったロジックで生成してストレージに保存したいけどとりあえずこの実装
    sessionId = base64.b64encode(user.email.encode())
    return {'sessionId': sessionId}

@app.post("/login")
def login(user: loginUser):
    try:
        encrypted_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM USERS WHERE(email = %s AND encrypted_password = %s)', (user.email, encrypted_password))
                result = cur.fetchall()
        if len(result) == 0:
            raise HTTPException(status_code=401, detail="User not exists")
        # sessionIdは本当はもう少し凝ったロジックで生成してストレージに保存したいけどとりあえずこの実装
        sessionId = base64.b64encode(user.email.encode())
        return {'sessionId': sessionId}
    except:
        return {'errMessage': 'login failure'}
