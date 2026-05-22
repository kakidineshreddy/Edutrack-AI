import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Student Schemas
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    grade_level: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    grade_level: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True
        orm_mode = True

# Teacher Schemas
class TeacherBase(BaseModel):
    name: str
    email: EmailStr
    subject: str

class TeacherCreate(TeacherBase):
    password: str

class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    subject: Optional[str] = None
    password: Optional[str] = None

class TeacherResponse(TeacherBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True
        orm_mode = True

# Course Schemas
class CourseBase(BaseModel):
    name: str
    teacher_id: Optional[int] = None
    schedule: str
    credits: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    teacher_id: Optional[int] = None
    schedule: Optional[str] = None
    credits: Optional[int] = None

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True

# Grade Schemas
class GradeBase(BaseModel):
    student_id: int
    course_id: int
    score: float

class GradeCreate(GradeBase):
    pass

class GradeUpdate(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    score: Optional[float] = None

class GradeResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    score: float
    letter_grade: str
    date: datetime.datetime
    student: Optional[StudentResponse] = None
    course: Optional[CourseResponse] = None

    class Config:
        from_attributes = True
        orm_mode = True

# Attendance Schemas
class AttendanceBase(BaseModel):
    student_id: int
    course_id: int
    status: str  # present, absent, late
    date: datetime.datetime

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    status: Optional[str] = None
    date: Optional[datetime.datetime] = None

class AttendanceResponse(AttendanceBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True

# Analytics / Extra Response Schemas
class StudentPerformance(BaseModel):
    student_id: int
    name: str
    email: str
    grade_level: str
    average_score: float
    attendance_rate: float
    at_risk: bool

class PredictionResponse(BaseModel):
    student_id: int
    predicted_score: float
    trend: str  # improving, declining, stable

class SubjectTips(BaseModel):
    subject: str
    tips: List[str]

class RecommendationsResponse(BaseModel):
    student_id: int
    recommendations: List[SubjectTips]
