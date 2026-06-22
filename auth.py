from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from database import cursor, connection
from dotenv import load_dotenv
import os



load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

security = HTTPBearer()

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


@auth_router.post("/register")
def register(payload: RegisterRequest):

    cursor.execute(
        "SELECT id FROM users WHERE email=%s",
        (payload.email,)
    )
    existing_user = cursor.fetchone()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    hashed_password = hash_password(payload.password)

    query = """
    INSERT INTO users(name,email,password)
    VALUES(%s,%s,%s)
    """

    values = (
        payload.name,
        payload.email,
        hashed_password
    )

    cursor.execute(query, values)
    connection.commit()

    return {
        "message": "User registered successfully"
    }


@auth_router.post("/login")
def login(payload: LoginRequest):

    query = """
    SELECT id,name,email,password
    FROM users
    WHERE email=%s
    """

    cursor.execute(query, (payload.email,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    if not verify_password(
            payload.password,
            user[3]):

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token(
        {
            "sub": str(user[0]),
            "email": user[2]
        }
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }


def verify_token(
        credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token"
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        return payload

    except JWTError:
        raise credentials_exception


def get_current_user(
        current_user=Depends(verify_token)):

    user_id = int(current_user["sub"])

    cursor.execute(
        "SELECT * FROM users WHERE id=%s",
        (user_id,)
    )
    user = cursor.fetchone()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user


@auth_router.get("/profile")
def profile(
        current_user=Depends(get_current_user)):

    return {
        "id": current_user[0],
        "name": current_user[1],
        "email": current_user[2],
        "age": current_user[3],
        "phone": current_user[4],
        "gender": current_user[5],
        "address": current_user[6],
        "city": current_user[7],
        "state": current_user[8],
        "country": current_user[9],
        "pincode": current_user[10]
    }








# from datetime import datetime, timedelta, timezone
# from typing import Optional
# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from jose import JWTError, jwt
# from pydantic import BaseModel
# from database import cursor

# SECRET_KEY = "mysecretkey"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# security = HTTPBearer()
# auth_router = APIRouter(tags=["auth"])


# class LoginRequest(BaseModel):
#     email: str


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()

#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(
#             minutes=ACCESS_TOKEN_EXPIRE_MINUTES
#         )

#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# @auth_router.post("/login")
# def login(payload: LoginRequest):
#     query = "SELECT id, name, email FROM users WHERE email = %s"
#     cursor.execute(query, (payload.email,))
#     user = cursor.fetchone()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid email"
#         )

#     token = create_access_token(
#         data={
#             "sub": str(user[0]),
#             "email": user[2]
#         }
#     )

#     return {
#         "access_token": token,
#         "token_type": "bearer"
#     }


# def verify_token(
#     credentials: HTTPAuthorizationCredentials = Depends(security)
# ):
#     token = credentials.credentials

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid or missing token",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub")

#         if user_id is None:
#             raise credentials_exception

#         return payload

#     except JWTError:
#         raise credentials_exception
    
    
    
    
#     Login with email
# ↓
# Check email in users table
# ↓
# Create JWT token
# ↓
# Send token back
# ↓
# Client sends token in Authorization header
# ↓
# verify_token() checks token
# ↓
# If valid → API works
# ↓
# If invalid → 401 Unauthorized







    

# from datetime import datetime, timedelta, timezone
# from typing import Optional

# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from jose import JWTError, jwt
# from pydantic import BaseModel
# from passlib.context import CryptContext

# from database import cursor, connection


# SECRET_KEY = "mysecretkey"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# security = HTTPBearer()

# auth_router = APIRouter(
#     prefix="/auth",
#     tags=["Authentication"]
# )

# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )



# class RegisterRequest(BaseModel):
#     name: str
#     email: str
#     password: str


# class LoginRequest(BaseModel):
#     email: str
#     password: str


# def hash_password(password: str):
#     return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str):
#     return pwd_context.verify(
#         plain_password,
#         hashed_password
#     )



# def create_access_token(
#         data: dict,
#         expires_delta: Optional[timedelta] = None):

#     to_encode = data.copy()

#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = (
#             datetime.now(timezone.utc)
#             + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#         )

#     to_encode.update({"exp": expire})

#     encoded_jwt = jwt.encode(
#         to_encode,
#         SECRET_KEY,
#         algorithm=ALGORITHM
#     )

#     return encoded_jwt


# @auth_router.post("/register")
# def register(payload: RegisterRequest):

#     query = """
#     SELECT email
#     FROM users
#     WHERE email=%s
#     """

#     cursor.execute(query, (payload.email,))
#     existing_user = cursor.fetchone()

#     if existing_user:
#         raise HTTPException(
#             status_code=400,
#             detail="Email already exists"
#         )

#     hashed_password = hash_password(payload.password)

#     query = """
#     INSERT INTO users(name,email,password)
#     VALUES(%s,%s,%s)
#     """

#     values = (
#         payload.name,
#         payload.email,
#         hashed_password
#     )

#     cursor.execute(query, values)
#     connection.commit()

#     return {
#         "message": "User registered successfully"
#     }


# @auth_router.post("/login")
# def login(payload: LoginRequest):

#     query = """
#     SELECT id,name,email,password
#     FROM users
#     WHERE email=%s
#     """

#     cursor.execute(query, (payload.email,))
#     user = cursor.fetchone()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid email"
#         )

#     password_valid = verify_password(
#         payload.password,
#         user[3]
#     )

#     if not password_valid:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid password"
#         )

#     token = create_access_token(
#         data={
#             "sub": str(user[0]),
#             "email": user[2]
#         }
#     )

#     return {
#         "access_token": token,
#         "token_type": "bearer"
#     }


# def verify_token(
#         credentials: HTTPAuthorizationCredentials = Depends(security)):

#     token = credentials.credentials

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid or Missing Token",
#         headers={"WWW-Authenticate": "Bearer"}
#     )

#     try:
#         payload = jwt.decode(
#             token,
#             SECRET_KEY,
#             algorithms=[ALGORITHM]
#         )

#         user_id = payload.get("sub")

#         if user_id is None:
#             raise credentials_exception

#         return payload

#     except JWTError:
#         raise credentials_exception


# @auth_router.get("/profile")
# def profile(current_user=Depends(verify_token)):

#     return {
#         "message": "Welcome",
#         "user": current_user
#     }



