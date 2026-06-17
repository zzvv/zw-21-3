from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import CourseSchedule
from app.schemas.schemas import CourseScheduleOut, CourseScheduleCreate
from app.routers.auth import get_current_user, require_role

router = APIRouter()

@router.get("", response_model=List[CourseScheduleOut])
def list_schedules(teacher_id: Optional[int] = None, classroom_id: Optional[int] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    q = db.query(CourseSchedule).filter(CourseSchedule.is_active == True)
    if teacher_id: q = q.filter(CourseSchedule.teacher_id == teacher_id)
    if classroom_id: q = q.filter(CourseSchedule.classroom_id == classroom_id)
    return q.order_by(CourseSchedule.weekday, CourseSchedule.start_time).all()

@router.post("", response_model=CourseScheduleOut)
def create_schedule(data: CourseScheduleCreate, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    s = CourseSchedule(**data.dict()); db.add(s); db.commit(); db.refresh(s); return s

@router.put("/{sid}", response_model=CourseScheduleOut)
def update_schedule(sid: int, data: CourseScheduleCreate, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    s = db.query(CourseSchedule).filter(CourseSchedule.id == sid).first()
    if not s: raise HTTPException(status_code=404, detail="排课不存在")
    for k, v in data.dict().items(): setattr(s, k, v)
    db.commit(); db.refresh(s); return s

@router.delete("/{sid}")
def delete_schedule(sid: int, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    s = db.query(CourseSchedule).filter(CourseSchedule.id == sid).first()
    if not s: raise HTTPException(status_code=404, detail="排课不存在")
    s.is_active = False; db.commit()
    return {"message": "排课已禁用"}
