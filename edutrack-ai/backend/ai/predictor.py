import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy.orm import Session
from backend.models import Grade

class PredictionEngine:
    @staticmethod
    def predict(student_id: int, db: Session):
        """
        Uses scikit-learn LinearRegression and numpy polyfit to fit the student's historical 
        grades and predict their next exam score. Evaluates academic performance trajectory.
        """
        try:
            # Query all grade entries for student sorted chronologically
            grades = db.query(Grade).filter(Grade.student_id == student_id).order_by(Grade.date.asc()).all()
            
            # Boundary case handling: less than 2 grades
            if not grades:
                return 75.0, "stable"
            if len(grades) < 2:
                # Return the sole score and a stable trend since slope cannot be calculated
                return float(grades[0].score), "stable"
                
            # Prepare data vectors
            # X represents exam sequence index (time step)
            # y represents exam scores
            X = np.array([[i] for i in range(len(grades))])
            y = np.array([[g.score] for g in grades])
            
            # 1. Fit scikit-learn linear regression model for next score prediction
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict score for next exam (index equal to len(grades))
            next_idx = np.array([[len(grades)]])
            prediction = model.predict(next_idx)
            predicted_score = float(prediction[0][0])
            
            # Bound predicted score logically within [0, 100]
            predicted_score = max(0.0, min(100.0, predicted_score))
            
            # 2. Fit using numpy polyfit to retrieve exact slope to determine trend
            x_flat = np.array([i for i in range(len(grades))])
            y_flat = np.array([g.score for g in grades])
            
            # Polyfit of degree 1 fits y = mx + c. slope is coefficient at index 0 (m)
            slope, _ = np.polyfit(x_flat, y_flat, 1)
            
            # Determine performance trend based on slope velocity
            if slope > 0.5:
                trend = "improving"
            elif slope < -0.5:
                trend = "declining"
            else:
                trend = "stable"
                
            return predicted_score, trend
            
        except Exception:
            # Fallback safe values in case of mathematical anomalies
            return 70.0, "stable"
