from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import Enrollment
from app.schemas.schemas import EnrollmentOut, EnrollmentCreate
from app.routers.auth import get_current_user, require_role

router = APIRouter()

@router.get("", response_model=List[EnrollmentOut])
def list_enrollments(student_id: Optional[int] = None, status: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    q = db.query(Enrollment)
    if student_id: q = q.filter(Enrollment.student_id == student_id)
    if status: q = q.filter(Enrollment.status == status)
    return q.order_by(Enrollment.created_at.desc()).all()

@router.post("", response_model=EnrollmentOut)
def create_enrollment(data: EnrollmentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    e = Enrollment(**data.dict()); db.add(e); db.commit(); db.refresh(e); return e

@router.post("/{eid}/consume")
def consume_lesson(eid: int, db: Session = Depends(get_db), _=require_role("admin", "manager", "teacher")):
    e = db.query(Enrollment).filter(Enrollment.id == eid).first()
    if not e: raise HTTPException(status_code=404, detail="报名不存在")
    if e.used_lessons >= e.total_lessons:
        raise HTTPException(status_code=400, detail="课时已用完")
    e.used_lessons += 1
    if e.used_lessons >= e.total_lessons:
        e.status = "completed"
    db.commit()
    return {"message": "扣课成功", "used_lessons": e.used_lessons}

@router.post("/{eid}/cancel")
def cancel_enrollment(eid: int, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    e = db.query(Enrollment).filter(Enrollment.id == eid).first()
    if not e: raise HTTPException(status_code=404, detail="报名不存在")
    e.status = "cancelled"; db.commit()
    return {"message": "报名已取消"}
