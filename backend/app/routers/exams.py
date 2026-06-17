from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.models.models import ExamRecord
from app.schemas.schemas import ExamRecordOut, ExamRecordCreate
from app.routers.auth import get_current_user, require_role

router = APIRouter()

@router.get("", response_model=List[ExamRecordOut])
def list_exams(student_id: Optional[int] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    q = db.query(ExamRecord).order_by(ExamRecord.exam_date.desc())
    if student_id: q = q.filter(ExamRecord.student_id == student_id)
    return q.all()

@router.post("", response_model=ExamRecordOut)
def create_exam(data: ExamRecordCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    e = ExamRecord(**data.dict()); db.add(e); db.commit(); db.refresh(e); return e

@router.put("/{eid}", response_model=ExamRecordOut)
def update_exam(eid: int, data: ExamRecordCreate, db: Session = Depends(get_db), _=require_role("admin", "manager", "teacher")):
    e = db.query(ExamRecord).filter(ExamRecord.id == eid).first()
    if not e: raise HTTPException(status_code=404, detail="考级记录不存在")
    for k, v in data.dict().items(): setattr(e, k, v)
    db.commit(); db.refresh(e); return e

@router.delete("/{eid}")
def delete_exam(eid: int, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    e = db.query(ExamRecord).filter(ExamRecord.id == eid).first()
    if not e: raise HTTPException(status_code=404, detail="考级记录不存在")
    db.delete(e); db.commit()
    return {"message": "考级记录已删除"}
