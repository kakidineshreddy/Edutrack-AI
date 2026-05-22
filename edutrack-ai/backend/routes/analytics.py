from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Student, Grade, Attendance, User
from backend.schemas import StudentPerformance, PredictionResponse, RecommendationsResponse
from backend.auth import get_current_user
from backend.ai.predictor import PredictionEngine
from backend.ai.recommendations import RecommendationEngine

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/performance", response_model=List[StudentPerformance])
def get_performance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        students = db.query(Student).all()
        performance_list = []
        
        for student in students:
            # Calculate average score
            grades = db.query(Grade).filter(Grade.student_id == student.id).all()
            avg_score = 0.0
            if grades:
                avg_score = sum(g.score for g in grades) / len(grades)
                
            # Calculate attendance rate
            attendance_records = db.query(Attendance).filter(Attendance.student_id == student.id).all()
            attendance_rate = 100.0
            if attendance_records:
                attended = sum(1 for r in attendance_records if r.status in ["present", "late"])
                attendance_rate = (attended / len(attendance_records)) * 100.0
                
            # Determine if at-risk (avg score < 60)
            at_risk = avg_score < 60.0
            
            performance_list.append(StudentPerformance(
                student_id=student.id,
                name=student.name,
                email=student.email,
                grade_level=student.grade_level,
                average_score=round(avg_score, 2),
                attendance_rate=round(attendance_rate, 2),
                at_risk=at_risk
            ))
            
        return performance_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error computing performance analytics: {str(e)}"
        )

@router.get("/predictions/{student_id}", response_model=PredictionResponse)
def get_student_prediction(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
            
        # Predict using core engine
        predicted_score, trend = PredictionEngine.predict(student_id, db)
        return PredictionResponse(
            student_id=student_id,
            predicted_score=round(predicted_score, 2),
            trend=trend
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing prediction models: {str(e)}"
        )

@router.get("/recommendations/{student_id}", response_model=RecommendationsResponse)
def get_student_recommendations(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found"
            )
            
        # Get recommendations
        recommendations = RecommendationEngine.get_recommendations(student_id, db)
        return RecommendationsResponse(
            student_id=student_id,
            recommendations=recommendations
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error compiling academic recommendations: {str(e)}"
        )
