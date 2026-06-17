from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.models import User
from app.schemas.schemas import UserOut, UserCreate
from app.routers.auth import get_current_user, require_role

router = APIRouter()

@router.get("", response_model=List[UserOut])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(User).offset(skip).limit(limit).all()

@router.post("", response_model=UserOut)
def create_user(data: UserCreate, db: Session = Depends(get_db), _: User = require_role("admin")):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = User(username=data.username, password_hash=get_password_hash(data.password), real_name=data.real_name, phone=data.phone, role=data.role)
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _: User = require_role("admin")):
    user = db.query(User).filter(User.id == user_id).first()
    if not user: raise HTTPException(status_code=404, detail="用户不存在")
    user.is_active = False; db.commit()
    return {"message": "用户已禁用"}
