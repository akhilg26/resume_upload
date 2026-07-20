from fastapi import APIRouter, HTTPException
import psycopg2
from app.models.user import UserRegister
import bcrypt
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

# jwt_secret = os.getenv('JWT_SECRET')
db_connection = os.getenv('SUPABASE')

router = APIRouter()


@router.post('/register')
def register(user: UserRegister):
    password_bytes = user.password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)


    conn = psycopg2.connect(db_connection)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
    result = cursor.fetchone()
    if result != None:
        raise HTTPException(
            status_code=409,
            detail='Username already taken'
        )
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id;",
        (user.username, hashed_password)
    )
    id = cursor.fetchone()
    conn.commit()
    return {'id': id[0]}