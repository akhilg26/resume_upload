import jwt
from fastapi import HTTPException, Header
from dotenv import load_dotenv
import os

load_dotenv()
jwt_secret = os.getenv("JWT_SECRET")


def verify_token(authorization: str = Header(None)): # basically, authorization looks for authorization (case-insensitive), matches it in the header, returns none if none exists, and then returns Bearer {token}
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Access not authorized: please login or register"
        )

    token = authorization.split(' ')[1]
    try:
        decoded_token = jwt.decode(token, jwt_secret, algorithms=['HS256'])
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Access denied; token invalid"
        )
    
    return int(decoded_token['sub'])