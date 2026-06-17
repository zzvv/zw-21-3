from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta
from app.core.database import get_db
from app.models.models import Classroom, CourseSchedule
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

@router.get("/board")
def classroom_board(target_date: Optional[date] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if target_date is None:
        target_date = date.today()
    weekday = target_date.weekday()
    
    classrooms = db.query(Classroom).order_by(Classroom.name).all()
    schedules = db.query(CourseSchedule)\
        .filter(CourseSchedule.is_active == True)\
        .filter(CourseSchedule.weekday == weekday)\
        .filter(CourseSchedule.start_date <= target_date)\
        .filter((CourseSchedule.end_date == None) | (CourseSchedule.end_date >= target_date))\
        .order_by(CourseSchedule.classroom_id, CourseSchedule.start_time)\
        .all()
    
    time_slots = [
        {"start": "08:00", "end": "09:00"},
        {"start": "09:00", "end": "10:00"},
        {"start": "10:00", "end": "11:00"},
        {"start": "11:00", "end": "12:00"},
        {"start": "13:00", "end": "14:00"},
        {"start": "14:00", "end": "15:00"},
        {"start": "15:00", "end": "16:00"},
        {"start": "16:00", "end": "17:00"},
        {"start": "17:00", "end": "18:00"},
        {"start": "18:00", "end": "19:00"},
        {"start": "19:00", "end": "20:00"},
        {"start": "20:00", "end": "21:00"},
    ]
    
    result = []
    for classroom in classrooms:
        room_schedules = [s for s in schedules if s.classroom_id == classroom.id]
        room_slots = []
        
        for slot in time_slots:
            occupied = False
            occupied_by = None
            for s in room_schedules:
                if s.start_time <= slot["start"] and s.end_time >= slot["end"]:
                    occupied = True
                    occupied_by = {
                        "id": s.id,
                        "course_name": s.course.name,
                        "teacher_name": s.teacher.name,
                        "start_time": s.start_time,
                        "end_time": s.end_time,
                    }
                    break
            room_slots.append({
                "time": f"{slot['start']}-{slot['end']}",
                "start_time": slot["start"],
                "end_time": slot["end"],
                "occupied": occupied,
                "schedule": occupied_by,
            })
        
        result.append({
            "id": classroom.id,
            "name": classroom.name,
            "capacity": classroom.capacity,
            "piano_count": classroom.piano_count,
            "status": classroom.status,
            "slots": room_slots,
        })
    
    return {"date": target_date, "weekday": weekday, "classrooms": result}
