from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import Teacher
from app.schemas.schemas import TeacherOut, TeacherCreate
from app.routers.auth import get_current_user, require_role

router = APIRouter()

@router.get("", response_model=List[TeacherOut])
def list_teachers(instrument: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    q = db.query(Teacher).filter(Teacher.is_active == True)
    if instrument: q = q.filter(Teacher.instrument == instrument)
    return q.all()

@router.post("", response_model=TeacherOut)
def create_teacher(data: TeacherCreate, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    t = Teacher(**data.dict()); db.add(t); db.commit(); db.refresh(t); return t

@router.put("/{tid}", response_model=TeacherOut)
def update_teacher(tid: int, data: TeacherCreate, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    t = db.query(Teacher).filter(Teacher.id == tid).first()
    if not t: raise HTTPException(status_code=404, detail="教师不存在")
    for k, v in data.dict().items(): setattr(t, k, v)
    db.commit(); db.refresh(t); return t

@router.delete("/{tid}")
def delete_teacher(tid: int, db: Session = Depends(get_db), _=require_role("admin")):
    t = db.query(Teacher).filter(Teacher.id == tid).first()
    if not t: raise HTTPException(status_code=404, detail="教师不存在")
    t.is_active = False; db.commit()
    return {"message": "教师已禁用"}
