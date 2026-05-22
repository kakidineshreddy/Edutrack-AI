from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Teacher, User
from backend.schemas import TeacherCreate, TeacherUpdate, TeacherResponse
from backend.auth import get_current_user, get_password_hash

router = APIRouter(prefix="/api/teachers", tags=["teachers"])

@router.get("", response_model=List[TeacherResponse])
def get_teachers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        teachers = db.query(Teacher).all()
        return teachers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving teachers: {str(e)}"
        )

@router.get("/{teacher_id}", response_model=TeacherResponse)
def get_teacher(teacher_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Teacher with ID {teacher_id} not found"
            )
        return teacher
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving teacher: {str(e)}"
        )

@router.post("", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(teacher_data: TeacherCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Check if email is already in use by a teacher
        existing_teacher = db.query(Teacher).filter(Teacher.email == teacher_data.email).first()
        if existing_teacher:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {teacher_data.email} is already in use"
            )
        
        hashed_password = get_password_hash(teacher_data.password)
        
        # Create teacher record
        new_teacher = Teacher(
            name=teacher_data.name,
            email=teacher_data.email,
            subject=teacher_data.subject,
            password_hash=hashed_password
        )
        db.add(new_teacher)
        
        # Also create a corresponding system User if not already present
        existing_user = db.query(User).filter(User.email == teacher_data.email).first()
        if not existing_user:
            new_user = User(
                email=teacher_data.email,
                password_hash=hashed_password,
                role="teacher"
            )
            db.add(new_user)
            
        db.commit()
        db.refresh(new_teacher)
        return new_teacher
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating teacher: {str(e)}"
        )

@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher(teacher_id: int, teacher_data: TeacherUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Teacher with ID {teacher_id} not found"
            )
        
        # Validate email uniqueness if changing
        if teacher_data.email and teacher_data.email != teacher.email:
            existing_teacher = db.query(Teacher).filter(Teacher.email == teacher_data.email).first()
            if existing_teacher:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email {teacher_data.email} is already in use"
                )
        
        # Extract data to update
        update_dict = teacher_data.model_dump(exclude_unset=True)
        
        # If updating password, hash it and update corresponding User if exists
        if "password" in update_dict and update_dict["password"]:
            new_hash = get_password_hash(update_dict["password"])
            teacher.password_hash = new_hash
            
            # Sync user model
            user = db.query(User).filter(User.email == teacher.email).first()
            if user:
                user.password_hash = new_hash
                if teacher_data.email:
                    user.email = teacher_data.email
            
            del update_dict["password"]
            
        # Update other teacher fields
        for key, value in update_dict.items():
            setattr(teacher, key, value)
            
        # Also sync User email if changed and no password update happened
        if teacher_data.email and teacher_data.email != teacher.email:
            user = db.query(User).filter(User.email == teacher.email).first()
            if user:
                user.email = teacher_data.email
                
        db.commit()
        db.refresh(teacher)
        return teacher
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating teacher: {str(e)}"
        )

@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Teacher with ID {teacher_id} not found"
            )
        
        # Delete user record associated with teacher email
        user = db.query(User).filter(User.email == teacher.email).first()
        if user:
            db.delete(user)
            
        db.delete(teacher)
        db.commit()
        return {"message": f"Teacher with ID {teacher_id} successfully deleted"}
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting teacher: {str(e)}"
        )
