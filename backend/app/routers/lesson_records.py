from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.models.models import LessonRecord
from app.schemas.schemas import LessonRecordOut, LessonRecordCreate
from app.routers.auth import get_current_user, require_role

router = APIRouter()

@router.get("", response_model=List[LessonRecordOut])
def list_records(enrollment_id: Optional[int] = None, start: Optional[date] = None, end: Optional[date] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    q = db.query(LessonRecord).order_by(LessonRecord.lesson_date.desc())
    if enrollment_id: q = q.filter(LessonRecord.enrollment_id == enrollment_id)
    if start: q = q.filter(LessonRecord.lesson_date >= start)
    if end: q = q.filter(LessonRecord.lesson_date <= end)
    return q.all()

@router.post("", response_model=LessonRecordOut)
def create_record(data: LessonRecordCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    r = LessonRecord(**data.dict()); db.add(r); db.commit(); db.refresh(r); return r

@router.put("/{rid}", response_model=LessonRecordOut)
def update_record(rid: int, data: LessonRecordCreate, db: Session = Depends(get_db), _=require_role("admin", "manager", "teacher")):
    r = db.query(LessonRecord).filter(LessonRecord.id == rid).first()
    if not r: raise HTTPException(status_code=404, detail="记录不存在")
    for k, v in data.dict().items(): setattr(r, k, v)
    db.commit(); db.refresh(r); return r

@router.delete("/{rid}")
def delete_record(rid: int, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    r = db.query(LessonRecord).filter(LessonRecord.id == rid).first()
    if not r: raise HTTPException(status_code=404, detail="记录不存在")
    db.delete(r); db.commit()
    return {"message": "记录已删除"}
