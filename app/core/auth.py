from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import secrets
import hashlib
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")



pwd_context =  CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90

def hash_pass(password: str) -> str:
    return pwd_context.hash(password)

def verify_pass(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_api_key():
    import secrets
    raw_key = secrets.token_urlsafe(32)
    hashed = hash_pass(raw_key)
    return raw_key, hashed