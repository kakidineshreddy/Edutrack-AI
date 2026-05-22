from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Course, Teacher, User
from backend.schemas import CourseCreate, CourseUpdate, CourseResponse
from backend.auth import get_current_user

router = APIRouter(prefix="/api/courses", tags=["courses"])

@router.get("", response_model=List[CourseResponse])
def get_courses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        courses = db.query(Course).all()
        return courses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving courses: {str(e)}"
        )

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found"
            )
        return course
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving course: {str(e)}"
        )

@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course_data: CourseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Check if teacher exists if teacher_id is provided
        if course_data.teacher_id:
            teacher = db.query(Teacher).filter(Teacher.id == course_data.teacher_id).first()
            if not teacher:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Teacher with ID {course_data.teacher_id} does not exist"
                )
                
        new_course = Course(
            name=course_data.name,
            teacher_id=course_data.teacher_id,
            schedule=course_data.schedule,
            credits=course_data.credits
        )
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating course: {str(e)}"
        )

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course_data: CourseUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found"
            )
            
        # Verify teacher exists if teacher_id is being updated
        if course_data.teacher_id:
            teacher = db.query(Teacher).filter(Teacher.id == course_data.teacher_id).first()
            if not teacher:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Teacher with ID {course_data.teacher_id} does not exist"
                )
                
        for key, value in course_data.model_dump(exclude_unset=True).items():
            setattr(course, key, value)
            
        db.commit()
        db.refresh(course)
        return course
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating course: {str(e)}"
        )

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found"
            )
            
        db.delete(course)
        db.commit()
        return {"message": f"Course with ID {course_id} successfully deleted"}
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting course: {str(e)}"
        )
