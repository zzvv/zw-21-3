from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import Course
from app.schemas.schemas import CourseOut, CourseCreate
from app.routers.auth import get_current_user, require_role

router = APIRouter()

@router.get("", response_model=List[CourseOut])
def list_courses(instrument: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    q = db.query(Course).filter(Course.is_active == True)
    if instrument: q = q.filter(Course.instrument == instrument)
    return q.all()

@router.post("", response_model=CourseOut)
def create_course(data: CourseCreate, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    c = Course(**data.dict()); db.add(c); db.commit(); db.refresh(c); return c

@router.put("/{cid}", response_model=CourseOut)
def update_course(cid: int, data: CourseCreate, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    c = db.query(Course).filter(Course.id == cid).first()
    if not c: raise HTTPException(status_code=404, detail="课程不存在")
    for k, v in data.dict().items(): setattr(c, k, v)
    db.commit(); db.refresh(c); return c

@router.delete("/{cid}")
def delete_course(cid: int, db: Session = Depends(get_db), _=require_role("admin")):
    c = db.query(Course).filter(Course.id == cid).first()
    if not c: raise HTTPException(status_code=404, detail="课程不存在")
    c.is_active = False; db.commit()
    return {"message": "课程已禁用"}
