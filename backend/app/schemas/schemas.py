from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    username: str
    real_name: Optional[str] = None
    phone: Optional[str] = None
    role: str
    is_active: bool
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str
    real_name: Optional[str] = None
    phone: Optional[str] = None
    role: str = "teacher"

class TeacherOut(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    instrument: Optional[str] = None
    level: Optional[str] = None
    bio: Optional[str] = None
    hire_date: Optional[date] = None
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class TeacherCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    instrument: Optional[str] = None
    level: Optional[str] = None
    bio: Optional[str] = None
    hire_date: Optional[date] = None

class StudentOut(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    birthday: Optional[date] = None
    level: Optional[str] = None
    remark: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    birthday: Optional[date] = None
    level: Optional[str] = None
    remark: Optional[str] = None

class CourseOut(BaseModel):
    id: int
    name: str
    instrument: Optional[str] = None
    duration_minutes: int
    price: Decimal
    max_students: int
    teacher_id: int
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    teacher: Optional[TeacherOut] = None
    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    name: str
    instrument: Optional[str] = None
    duration_minutes: int = 45
    price: Decimal = Decimal("0")
    max_students: int = 1
    teacher_id: int
    description: Optional[str] = None

class ClassroomOut(BaseModel):
    id: int
    name: str
    capacity: int
    piano_count: int
    status: str
    remark: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class ClassroomCreate(BaseModel):
    name: str
    capacity: int = 4
    piano_count: int = 1
    remark: Optional[str] = None

class CourseScheduleOut(BaseModel):
    id: int
    course_id: int
    classroom_id: int
    teacher_id: int
    weekday: int
    start_time: str
    end_time: str
    start_date: date
    end_date: Optional[date] = None
    is_active: bool
    created_at: datetime
    course: Optional[CourseOut] = None
    classroom: Optional[ClassroomOut] = None
    teacher: Optional[TeacherOut] = None
    class Config:
        from_attributes = True

class CourseScheduleCreate(BaseModel):
    course_id: int
    classroom_id: int
    teacher_id: int
    weekday: int
    start_time: str
    end_time: str
    start_date: date
    end_date: Optional[date] = None

class EnrollmentOut(BaseModel):
    id: int
    student_id: int
    course_id: int
    schedule_id: int
    total_lessons: int
    used_lessons: int
    amount: Decimal
    status: str
    created_at: datetime
    student: Optional[StudentOut] = None
    course: Optional[CourseOut] = None
    schedule: Optional[CourseScheduleOut] = None
    class Config:
        from_attributes = True

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    schedule_id: int
    total_lessons: int = 12
    amount: Decimal = Decimal("0")

class LessonRecordOut(BaseModel):
    id: int
    enrollment_id: int
    lesson_date: date
    status: str
    content: Optional[str] = None
    homework: Optional[str] = None
    created_at: datetime
    enrollment: Optional[EnrollmentOut] = None
    class Config:
        from_attributes = True

class LessonRecordCreate(BaseModel):
    enrollment_id: int
    lesson_date: date
    status: str = "attended"
    content: Optional[str] = None
    homework: Optional[str] = None

class ExamRecordOut(BaseModel):
    id: int
    student_id: int
    exam_name: str
    instrument: Optional[str] = None
    level: Optional[str] = None
    exam_date: Optional[date] = None
    result: Optional[str] = None
    score: Optional[str] = None
    certificate_no: Optional[str] = None
    remark: Optional[str] = None
    created_at: datetime
    student: Optional[StudentOut] = None
    class Config:
        from_attributes = True

class ExamRecordCreate(BaseModel):
    student_id: int
    exam_name: str
    instrument: Optional[str] = None
    level: Optional[str] = None
    exam_date: Optional[date] = None
    result: Optional[str] = None
    score: Optional[str] = None
    certificate_no: Optional[str] = None
    remark: Optional[str] = None

class InstrumentOut(BaseModel):
    id: int
    name: str
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_no: Optional[str] = None
    status: str
    purchase_date: Optional[date] = None
    price: Decimal
    remark: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class InstrumentCreate(BaseModel):
    name: str
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_no: Optional[str] = None
    purchase_date: Optional[date] = None
    price: Decimal = Decimal("0")
    remark: Optional[str] = None

class DashboardStats(BaseModel):
    total_students: int
    total_teachers: int
    total_courses: int
    active_enrollments: int
    today_lessons: int
    pending_exams: int
    low_stock_instruments: int
    monthly_revenue: Decimal

class RecentLesson(BaseModel):
    lesson_date: date
    student_name: str
    course_name: str
    status: str

class DashboardOut(BaseModel):
    stats: DashboardStats
    weekly_schedule: List[CourseScheduleOut]
    recent_lessons: List[LessonRecordOut]
    low_stock_instruments: List[InstrumentOut]
