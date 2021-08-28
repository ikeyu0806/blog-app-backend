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
    user_id: int

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
            cur.execute('INSERT INTO posts (title, content, user_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)', (post.title, post.content, post.user_id, dt, dt))
        conn.commit()
    return {"post": post}

@app.get("/posts")
def posts():
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT posts.id, posts.title, posts.content, users.name as user_name  FROM posts left outer join users on posts.user_id = users.id')
            result = cur.fetchall()

    key = ["id", "title", "content", "user_name"]
    result = [dict(zip(key, post)) for post in result]

    return {'posts': result}

@app.get("/post/{post_id}")
def post_detail(post_id):
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM posts WHERE id = %s', (post_id))
            result = cur.fetchone()

    key = ["id", "title", "content"]
    result = [dict(zip(key, list(result)))][0]

    return {'post': result}

@app.post("/create_user")
def create_user(user: createUser):
    try:
        dt = datetime.datetime.now()
        encrypted_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO users (name, email, encrypted_password, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)', (user.name, user.email, encrypted_password, dt, dt))
            conn.commit()

        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM users WHERE email = %s AND encrypted_password = %s LIMIT 1', (user.email, encrypted_password))
                result = cur.fetchone()
        # sessionIdは本当はもう少し凝ったロジックで生成してストレージに保存したいけどとりあえずこの実装
        sessionId = base64.b64encode(user.email.encode())
        return {'sessionId': sessionId, 'user_name': result[1], 'user_id': result[0]}
    except:
        return {'errMessage': 'signup failure'}

@app.post("/login")
def login(user: loginUser):
    try:
        encrypted_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM users WHERE email = %s AND encrypted_password = %s LIMIT 1', (user.email, encrypted_password))
                result = cur.fetchone()

        if result is None:
            raise HTTPException(status_code=401, detail="User not exists")

        # sessionIdは本当はもう少し凝ったロジックで生成してストレージに保存したいけどとりあえずこの実装
        sessionId = base64.b64encode(user.email.encode())
        return {'sessionId': sessionId, 'user_name': result[1], 'user_id': result[0]}
    except:
        return {'errMessage': 'login failure'}

@app.get("/users")
def users():
    with db.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM users')
            result = cur.fetchall()

    key = ["id", "name"]
    result = [dict(zip(key, user)) for user in result]

    return {'users': result}
