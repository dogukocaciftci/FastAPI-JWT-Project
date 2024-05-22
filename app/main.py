# Main Method
from fastapi import FastAPI, Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

from .middleware import JWTBearer
from .auth import verify_password, users
from .config import SECRET_KEY, ALGORITHM, JWT_TIMEOUT

# Creating a FastAPI application
app = FastAPI()

# Defining the Token model


class Token(BaseModel):
    access_token: str
    token_type: str

# Defining the TokenData model


class TokenData(BaseModel):
    username: Optional[str] = None

# Defining the User model


class User(BaseModel):
    username: str
    password: str

# User login endpoint


@app.post("/token", response_model=Token)
async def login(user: User):
    # User validation
    stored_password = users.get(user.username)
    if not stored_password or not verify_password(user.password, stored_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    # Creating the access token
    access_token_expires = timedelta(minutes=JWT_TIMEOUT)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Example of a protected endpoint


@app.get("/protected", dependencies=[Depends(JWTBearer())])
async def protected_route():
    return {"message": "You are authorized"}

# Function to create an access token


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
