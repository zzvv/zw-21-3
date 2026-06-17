from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import Student
from app.schemas.schemas import StudentOut, StudentCreate
from app.routers.auth import get_current_user, require_role

router = APIRouter()

@router.get("", response_model=List[StudentOut])
def list_students(q: Optional[str] = None, level: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    query = db.query(Student)
    if q:
        query = query.filter((Student.name.contains(q)) | (Student.phone.contains(q)))
    if level:
        query = query.filter(Student.level == level)
    return query.order_by(Student.created_at.desc()).all()

@router.post("", response_model=StudentOut)
def create_student(data: StudentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    s = Student(**data.dict()); db.add(s); db.commit(); db.refresh(s); return s

@router.put("/{sid}", response_model=StudentOut)
def update_student(sid: int, data: StudentCreate, db: Session = Depends(get_db), _=require_role("admin", "manager", "teacher")):
    s = db.query(Student).filter(Student.id == sid).first()
    if not s: raise HTTPException(status_code=404, detail="学员不存在")
    for k, v in data.dict().items(): setattr(s, k, v)
    db.commit(); db.refresh(s); return s

@router.delete("/{sid}")
def delete_student(sid: int, db: Session = Depends(get_db), _=require_role("admin")):
    s = db.query(Student).filter(Student.id == sid).first()
    if not s: raise HTTPException(status_code=404, detail="学员不存在")
    db.delete(s); db.commit()
    return {"message": "学员已删除"}
