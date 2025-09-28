from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.auth.models import Auth
from app.auth.schemas import AuthCreate, AuthLogin, AuthRead
from app.auth.hash import hash_password, verify_password
from authx import AuthX, AuthXConfig  
from dotenv import load_dotenv
import os


load_dotenv()


router = APIRouter()

config = AuthXConfig()
config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

password_symbols = "!\"#$%&'()*+,-/:;<=>?@[\\]^{|}~"

@router.post("/register", response_model=AuthRead)
async def user_register(user: AuthCreate, db: Session = Depends(get_db)):
    if db.query(Auth).filter(Auth.login == user.login).first():
        raise HTTPException(status_code=400, detail="Логин уже занят")

    if db.query(Auth).filter(Auth.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email уже занят")

    for sym in password_symbols:
        if sym in user.password:
            raise HTTPException(status_code=400, detail="В пароле запрещенный символ")

    hashed = hash_password(user.password)

    db_user = Auth(login=user.login, email=user.email, password_hash=hashed)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login")
async def user_login(user: AuthLogin, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(Auth).filter(Auth.login == user.login).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Некорректный ввод пользователя или пароля")

    if db_user.email != user.email:
        raise HTTPException(status_code=401, detail="Пользователь не зарегистрирован под этот email")

    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Пароль неверный")

    token = security.create_access_token(uid=str(db_user.id))
    response.set_cookie(key="access_token", value=token, httponly=True)

    return {"message": "Login successful"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}