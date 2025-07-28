from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

SECURITY_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data : dict, expires_delta : Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp" : expire})
    return jwt.encode(to_encode, SECURITY_KEY, algorithm=ALGORITHM)

def decode_access_token(token : str):
    try:
        payload = jwt.decode(token, SECURITY_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        return None