from datetime import datetime, timedelta
from sqlmodel import SQLModel, Session
from fastapi.security import OAuth2PasswordBearer
from database import engine
import schemas
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
import models
from sqlmodel import select


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "a924c4a7c5e0019a69c15412b4f01dd451023fce957a606223ed390fdba1a809"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    session = get_session()
    user = next(session).exec(
        select(models.User).where(models.User.username == username)
    ).first()
    if user:
        print(user.username)
        return user
    else:
        print("No user found")


def check_user(userIn: schemas.UserInSchema):
    session = get_session()
    user_in_db = next(session).exec(
        select(models.User).where(models.User.username == userIn.username)
    ).first()
    if user_in_db:
        return user_in_db
    else:
        user_in_db = session.exec(
            select(models.User).where(models.User == userIn.email)
        ).first()
        if user_in_db:
            return user_in_db


def create_admin():
    session = get_session()
    admin = next(session).exec(
        select(models.User).where(models.User.is_admin == True)
    ).first()
    if not admin:
        new_user = models.User(
            username="admin",
            email="admin@gmail.com",
            full_name="Admin",
            is_admin=True,
            hashed_password=get_password_hash("COCAdmin")
        )
        next(session).add(new_user)
        next(session).commit()


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


async def get_current_admin_user(
    current_user: models.User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="Admin rights required")

    return current_user
