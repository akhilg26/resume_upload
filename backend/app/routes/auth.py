from fastapi import APIRouter, HTTPException
import psycopg2
from app.models.user import UserRegister
import bcrypt
import jwt
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

jwt_secret = os.getenv('JWT_SECRET')
db_connection = os.getenv('SUPABASE')

router = APIRouter()


@router.post('/register')
def register(user: UserRegister):
    password_bytes = user.password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    print("DB CONNECTION STRING:", db_connection)
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

    payload = {
        'sub': str(id[0]),
        'exp' : datetime.datetime.now() + datetime.timedelta(hours=24)
    }

    token = jwt.encode(payload, jwt_secret, algorithm='HS256')

    return {'token': token}

@router.post('/login')
def login(user: UserRegister):
    conn = psycopg2.connect(db_connection)
    cursor = conn.cursor()
    cursor.execute('SELECT id, password_hash FROM users WHERE username = %s', (user.username,))
    result = cursor.fetchone()
    if result == None:
        raise HTTPException(
            status_code=404,
            detail='Username does not exist'
        )
    password_bytes = user.password.encode('utf-8')
    if bcrypt.checkpw(password_bytes, result[1].encode('utf-8')) == False:
        raise HTTPException(
            status_code=401,
            detail='Incorrect password'
        )

    payload = {
        'sub': str(result[0]),
        'exp': datetime.datetime.now() + datetime.timedelta(hours=24)
    }

    token = jwt.encode(payload, jwt_secret, algorithm='HS256')

    return {'token': token}
    

    
