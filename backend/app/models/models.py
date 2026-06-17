from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    real_name = Column(String(50))
    phone = Column(String(20))
    role = Column(String(20), default='teacher')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20))
    instrument = Column(String(50))
    level = Column(String(20), default='intermediate')
    bio = Column(Text)
    hire_date = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    courses = relationship('Course', back_populates='teacher')

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20))
    parent_name = Column(String(50))
    parent_phone = Column(String(20))
    birthday = Column(Date)
    level = Column(String(20), default='beginner')
    remark = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    enrollments = relationship('Enrollment', back_populates='student')

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    instrument = Column(String(50))
    duration_minutes = Column(Integer, default=45)
    price = Column(Numeric(10, 2), default=0)
    max_students = Column(Integer, default=1)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    teacher = relationship('Teacher', back_populates='courses')

class Classroom(Base):
    __tablename__ = 'classrooms'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    capacity = Column(Integer, default=4)
    piano_count = Column(Integer, default=1)
    status = Column(String(20), default='available')
    remark = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)

class CourseSchedule(Base):
    __tablename__ = 'course_schedules'
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    classroom_id = Column(Integer, ForeignKey('classrooms.id'))
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    weekday = Column(Integer, nullable=False)
    start_time = Column(String(10), nullable=False)
    end_time = Column(String(10), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    course = relationship('Course')
    classroom = relationship('Classroom')
    teacher = relationship('Teacher')

class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    schedule_id = Column(Integer, ForeignKey('course_schedules.id'))
    total_lessons = Column(Integer, default=12)
    used_lessons = Column(Integer, default=0)
    amount = Column(Numeric(10, 2), default=0)
    status = Column(String(20), default='active')
    created_at = Column(DateTime, default=datetime.now)
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course')
    schedule = relationship('CourseSchedule')

class LessonRecord(Base):
    __tablename__ = 'lesson_records'
    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey('enrollments.id'))
    lesson_date = Column(Date, nullable=False)
    status = Column(String(20), default='attended')
    content = Column(Text)
    homework = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    enrollment = relationship('Enrollment')

class ExamRecord(Base):
    __tablename__ = 'exam_records'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    exam_name = Column(String(100), nullable=False)
    instrument = Column(String(50))
    level = Column(String(50))
    exam_date = Column(Date)
    result = Column(String(20))
    score = Column(String(20))
    certificate_no = Column(String(100))
    remark = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    student = relationship('Student')

class Instrument(Base):
    __tablename__ = 'instruments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    brand = Column(String(50))
    model = Column(String(50))
    serial_no = Column(String(100))
    status = Column(String(20), default='available')
    purchase_date = Column(Date)
    price = Column(Numeric(10, 2), default=0)
    remark = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
