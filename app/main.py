from fastapi import FastAPI, Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

from .middleware import JWTBearer
from .auth import verify_password, users
from .config import SECRET_KEY, ALGORITHM, JWT_TIMEOUT

# FastAPI uygulaması oluşturma
app = FastAPI()

# Token modelini tanımlama


class Token(BaseModel):
    access_token: str
    token_type: str

# Token verilerini tanımlama


class TokenData(BaseModel):
    username: Optional[str] = None

# Kullanıcı modelini tanımlama


class User(BaseModel):
    username: str
    password: str

# Kullanıcı giriş endpointi


@app.post("/token", response_model=Token)
async def login(user: User):
    # Kullanıcı doğrulama
    stored_password = users.get(user.username)
    if not stored_password or not verify_password(user.password, stored_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    # Access token oluşturma
    access_token_expires = timedelta(minutes=JWT_TIMEOUT)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Korumalı endpoint örneği


@app.get("/protected", dependencies=[Depends(JWTBearer())])
async def protected_route():
    return {"message": "You are authorized"}

# Access token oluşturma fonksiyonu


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
