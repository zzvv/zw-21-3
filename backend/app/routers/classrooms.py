from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import Classroom
from app.schemas.schemas import ClassroomOut, ClassroomCreate
from app.routers.auth import get_current_user, require_role

router = APIRouter()

@router.get("", response_model=List[ClassroomOut])
def list_classrooms(status: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    q = db.query(Classroom)
    if status: q = q.filter(Classroom.status == status)
    return q.all()

@router.post("", response_model=ClassroomOut)
def create_classroom(data: ClassroomCreate, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    c = Classroom(**data.dict()); db.add(c); db.commit(); db.refresh(c); return c

@router.put("/{cid}", response_model=ClassroomOut)
def update_classroom(cid: int, data: ClassroomCreate, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    c = db.query(Classroom).filter(Classroom.id == cid).first()
    if not c: raise HTTPException(status_code=404, detail="教室不存在")
    for k, v in data.dict().items(): setattr(c, k, v)
    db.commit(); db.refresh(c); return c

@router.post("/{cid}/status")
def update_status(cid: int, status: str, db: Session = Depends(get_db), _=require_role("admin", "manager", "teacher")):
    c = db.query(Classroom).filter(Classroom.id == cid).first()
    if not c: raise HTTPException(status_code=404, detail="教室不存在")
    c.status = status; db.commit()
    return {"message": "状态已更新"}

@router.delete("/{cid}")
def delete_classroom(cid: int, db: Session = Depends(get_db), _=require_role("admin")):
    c = db.query(Classroom).filter(Classroom.id == cid).first()
    if not c: raise HTTPException(status_code=404, detail="教室不存在")
    db.delete(c); db.commit()
    return {"message": "教室已删除"}
