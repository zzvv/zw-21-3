from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from sqlalchemy import func
from app.core.database import get_db
from app.models.models import Student, Teacher, Course, Enrollment, LessonRecord, ExamRecord, Instrument, CourseSchedule
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("")
def dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    total_students = db.query(Student).count()
    total_teachers = db.query(Teacher).filter(Teacher.is_active == True).count()
    total_courses = db.query(Course).filter(Course.is_active == True).count()
    active_enrollments = db.query(Enrollment).filter(Enrollment.status == "active").count()

    today = date.today()
    today_weekday = today.weekday()
    today_lessons = db.query(LessonRecord).filter(LessonRecord.lesson_date == today).count()

    upcoming_exams = db.query(ExamRecord).filter(ExamRecord.exam_date >= today, ExamRecord.exam_date <= today + timedelta(days=30)).count()
    low_stock = db.query(Instrument).filter(Instrument.status == "repair").count()

    month_start = today.replace(day=1)
    revenue = db.query(func.coalesce(func.sum(Enrollment.amount), 0)).filter(Enrollment.created_at >= month_start).scalar()

    weekly_schedule = db.query(CourseSchedule).filter(
        CourseSchedule.is_active == True,
        CourseSchedule.weekday == today_weekday
    ).order_by(CourseSchedule.start_time).all()

    recent_lessons = db.query(LessonRecord).order_by(LessonRecord.created_at.desc()).limit(5).all()
    low_stock_instruments = db.query(Instrument).filter(Instrument.status == "repair").order_by(Instrument.created_at.desc()).limit(5).all()

    return {
        "stats": {
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_courses": total_courses,
            "active_enrollments": active_enrollments,
            "today_lessons": today_lessons,
            "pending_exams": upcoming_exams,
            "low_stock_instruments": low_stock,
            "monthly_revenue": float(revenue or 0),
        },
        "weekly_schedule": weekly_schedule,
        "recent_lessons": recent_lessons,
        "low_stock_instruments": low_stock_instruments,
    }
