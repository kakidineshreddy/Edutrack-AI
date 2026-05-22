from typing import List
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Attendance, Student, Course, User
from backend.schemas import AttendanceCreate, AttendanceUpdate, AttendanceResponse
from backend.auth import get_current_user

router = APIRouter(prefix="/api/attendance", tags=["attendance"])

@router.get("", response_model=List[AttendanceResponse])
def get_attendance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        attendance_records = db.query(Attendance).all()
        return attendance_records
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving attendance: {str(e)}"
        )

@router.get("/student/{student_id}", response_model=List[AttendanceResponse])
def get_student_attendance(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
            
        records = db.query(Attendance).filter(Attendance.student_id == student_id).order_by(Attendance.date.desc()).all()
        return records
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving attendance for student: {str(e)}"
        )

@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance(attendance_data: AttendanceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == attendance_data.student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with ID {attendance_data.student_id} does not exist"
            )
            
        # Verify course exists
        course = db.query(Course).filter(Course.id == attendance_data.course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Course with ID {attendance_data.course_id} does not exist"
            )
            
        # Verify status is one of the valid options
        if attendance_data.status not in ["present", "absent", "late"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status must be one of: present, absent, late"
            )
            
        new_record = Attendance(
            student_id=attendance_data.student_id,
            course_id=attendance_data.course_id,
            status=attendance_data.status,
            date=attendance_data.date
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return new_record
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating attendance record: {str(e)}"
        )

@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(attendance_id: int, attendance_data: AttendanceUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance record with ID {attendance_id} not found"
            )
            
        # Verify student if updating
        if attendance_data.student_id:
            student = db.query(Student).filter(Student.id == attendance_data.student_id).first()
            if not student:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Student with ID {attendance_data.student_id} does not exist"
                )
                
        # Verify course if updating
        if attendance_data.course_id:
            course = db.query(Course).filter(Course.id == attendance_data.course_id).first()
            if not course:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Course with ID {attendance_data.course_id} does not exist"
                )
                
        # Verify status if updating
        if attendance_data.status and attendance_data.status not in ["present", "absent", "late"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status must be one of: present, absent, late"
            )
            
        for key, value in attendance_data.model_dump(exclude_unset=True).items():
            setattr(record, key, value)
            
        db.commit()
        db.refresh(record)
        return record
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating attendance record: {str(e)}"
        )

@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance record with ID {attendance_id} not found"
            )
            
        db.delete(record)
        db.commit()
        return {"message": f"Attendance record with ID {attendance_id} successfully deleted"}
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting attendance record: {str(e)}"
        )
