from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate, UserRead
from sqlalchemy import case, func


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        

@router.post('/users')
async def user_create(user: UserCreate, db: Session = Depends(get_db)):
    
    if db.query(User).filter(User.id == user.id).first():
        raise HTTPException(401, 'Такой юзер id уже зарегистрирован')
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(401, 'Такой юзернейм уже зарегистрирован')
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(401, 'Такой эмаил уже зарегистрирован')
    if db.query(User).filter(User.phone == user.phone).first():
        raise HTTPException(401, 'Такой номер уже зарегистрирован')
        
    db_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        role=user.role,
        department=user.department,
        telegram_chat_id=user.telegram_chat_id,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {'Message': f'Succesful Register: {user.username}'}



@router.get('/users/{id}')
async def get_user(id: str, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == id).all()


@router.put('/users/{id}', response_model=UserRead)
async def update_user(id: str, current: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(401, 'Такого юзер id нету')
    
    if current.username is not None:
        db_user.username = current.username
    if current.full_name is not None:
        db_user.full_name = current.full_name
    if current.email is not None:
        db_user.email = current.email
    if current.telegram_chat_id is not None:
        db_user.telegram_chat_id = current.telegram_chat_id
    if current.role is not None:
        db_user.role = current.role
    if current.department is not None:
        db_user.department = current.department
        
    db.commit()
    db.refresh(db_user)
    
    return db_user



priority_order = case(
    (func.lower(User.role) == "Руководитель отдела", 1),
    (func.lower(User.role) == "Сервис-менеджер", 2),
    (func.lower(User.role) == "Электрик", 3),
    (func.lower(User.role) == "Энергетик", 4),
    (func.lower(User.role) == "Специалист по отоплению", 5),
    else_=6
)

@router.get("/users")
async def users_info(db: Session = Depends(get_db)):
    return db.query(User).order_by(priority_order).all()
