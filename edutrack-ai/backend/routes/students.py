from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Student, User
from backend.schemas import StudentCreate, StudentUpdate, StudentResponse
from backend.auth import get_current_user

router = APIRouter(prefix="/api/students", tags=["students"])

@router.get("", response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        students = db.query(Student).all()
        return students
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving students: {str(e)}"
        )

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        return student
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving student: {str(e)}"
        )

@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student_data: StudentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Check if student email is already registered
        existing_student = db.query(Student).filter(Student.email == student_data.email).first()
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {student_data.email} is already in use by another student"
            )
        
        new_student = Student(
            name=student_data.name,
            email=student_data.email,
            grade_level=student_data.grade_level
        )
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating student: {str(e)}"
        )

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_data: StudentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        
        # Check if email update conflicts with another student
        if student_data.email and student_data.email != student.email:
            existing_student = db.query(Student).filter(Student.email == student_data.email).first()
            if existing_student:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email {student_data.email} is already in use by another student"
                )
        
        # Apply updates
        for key, value in student_data.model_dump(exclude_unset=True).items():
            setattr(student, key, value)
            
        db.commit()
        db.refresh(student)
        return student
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating student: {str(e)}"
        )

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
        
        db.delete(student)
        db.commit()
        return {"message": f"Student with ID {student_id} successfully deleted"}
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting student: {str(e)}"
        )
