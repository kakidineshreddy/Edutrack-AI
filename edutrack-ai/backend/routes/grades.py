from typing import List
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from backend.database import get_db
from backend.models import Grade, Student, Course, User
from backend.schemas import GradeCreate, GradeUpdate, GradeResponse
from backend.auth import get_current_user

router = APIRouter(prefix="/api/grades", tags=["grades"])

def calculate_letter_grade(score: float) -> str:
    if score >= 90.0:
        return "A"
    elif score >= 80.0:
        return "B"
    elif score >= 70.0:
        return "C"
    elif score >= 60.0:
        return "D"
    else:
        return "F"

@router.get("", response_model=List[GradeResponse])
def get_grades(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Load associated student and course models for comprehensive response representation
        grades = db.query(Grade).options(
            joinedload(Grade.student),
            joinedload(Grade.course)
        ).all()
        return grades
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving grades: {str(e)}"
        )

@router.get("/{grade_id}", response_model=GradeResponse)
def get_grade(grade_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        grade = db.query(Grade).options(
            joinedload(Grade.student),
            joinedload(Grade.course)
        ).filter(Grade.id == grade_id).first()
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grade record with ID {grade_id} not found"
            )
        return grade
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving grade: {str(e)}"
        )

@router.get("/student/{student_id}", response_model=List[GradeResponse])
def get_student_grades(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Verify student exists first
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
            
        grades = db.query(Grade).options(
            joinedload(Grade.student),
            joinedload(Grade.course)
        ).filter(Grade.student_id == student_id).order_by(Grade.date.desc()).all()
        return grades
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving student grades: {str(e)}"
        )

@router.post("", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
def create_grade(grade_data: GradeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == grade_data.student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with ID {grade_data.student_id} does not exist"
            )
            
        # Verify course exists
        course = db.query(Course).filter(Course.id == grade_data.course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Course with ID {grade_data.course_id} does not exist"
            )
            
        # Compute letter grade
        letter_grade = calculate_letter_grade(grade_data.score)
        
        new_grade = Grade(
            student_id=grade_data.student_id,
            course_id=grade_data.course_id,
            score=grade_data.score,
            letter_grade=letter_grade,
            date=datetime.datetime.utcnow()
        )
        db.add(new_grade)
        db.commit()
        db.refresh(new_grade)
        
        # Load relations before returning
        return db.query(Grade).options(
            joinedload(Grade.student),
            joinedload(Grade.course)
        ).filter(Grade.id == new_grade.id).first()
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating grade: {str(e)}"
        )

@router.put("/{grade_id}", response_model=GradeResponse)
def update_grade(grade_id: int, grade_data: GradeUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        grade = db.query(Grade).filter(Grade.id == grade_id).first()
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grade record with ID {grade_id} not found"
            )
            
        # Verify student if updating
        if grade_data.student_id:
            student = db.query(Student).filter(Student.id == grade_data.student_id).first()
            if not student:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Student with ID {grade_data.student_id} does not exist"
                )
                
        # Verify course if updating
        if grade_data.course_id:
            course = db.query(Course).filter(Course.id == grade_data.course_id).first()
            if not course:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Course with ID {grade_data.course_id} does not exist"
                )
                
        # Apply updates
        update_dict = grade_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(grade, key, value)
            
        # Recompute letter grade if score is updated
        if "score" in update_dict:
            grade.letter_grade = calculate_letter_grade(grade.score)
            
        db.commit()
        db.refresh(grade)
        
        # Load relations before returning
        return db.query(Grade).options(
            joinedload(Grade.student),
            joinedload(Grade.course)
        ).filter(Grade.id == grade.id).first()
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating grade: {str(e)}"
        )

@router.delete("/{grade_id}")
def delete_grade(grade_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        grade = db.query(Grade).filter(Grade.id == grade_id).first()
        if not grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grade record with ID {grade_id} not found"
            )
            
        db.delete(grade)
        db.commit()
        return {"message": f"Grade record with ID {grade_id} successfully deleted"}
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting grade: {str(e)}"
        )
