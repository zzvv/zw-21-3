from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routers import auth, users, teachers, students, courses, classrooms, schedules, enrollments, lesson_records, exams, instruments, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="琴行教务管理系统", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户"])
app.include_router(teachers.router, prefix="/api/teachers", tags=["教师"])
app.include_router(students.router, prefix="/api/students", tags=["学员"])
app.include_router(courses.router, prefix="/api/courses", tags=["课程"])
app.include_router(classrooms.router, prefix="/api/classrooms", tags=["教室"])
app.include_router(schedules.router, prefix="/api/schedules", tags=["排课"])
app.include_router(enrollments.router, prefix="/api/enrollments", tags=["报名"])
app.include_router(lesson_records.router, prefix="/api/lesson-records", tags=["上课记录"])
app.include_router(exams.router, prefix="/api/exams", tags=["考级"])
app.include_router(instruments.router, prefix="/api/instruments", tags=["乐器"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["看板"])

@app.get("/")
def root():
    return {"message": "琴行教务管理系统 API"}
