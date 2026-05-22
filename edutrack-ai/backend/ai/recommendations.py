from sqlalchemy.orm import Session
from backend.models import Grade, Course

class RecommendationEngine:
    @staticmethod
    def get_recommendations(student_id: int, db: Session):
        """
        Queries student scores grouped by course, aggregates average values per subject, 
        and dispenses three highly granular, subject-specific corrective strategies for 
        any course averages falling under 70%.
        """
        try:
            # Query all grade items for the target student
            grades = db.query(Grade).filter(Grade.student_id == student_id).all()
            
            # Group scores by course name
            course_scores = {}
            for grade in grades:
                course = db.query(Course).filter(Course.id == grade.course_id).first()
                if course:
                    if course.name not in course_scores:
                        course_scores[course.name] = []
                    course_scores[course.name].append(grade.score)
            
            recommendations = []
            
            # Concrete tips repository matching user requirements
            tips_bank = {
                "math": [
                    "Practice solving at least 5 algebraic and calculus problems daily to build muscle memory and pattern recognition.",
                    "Utilize curated video lectures on Khan Academy to reinforce foundational rules behind weak topics.",
                    "Build a comprehensive formula sheet, tracing mechanical derivations rather than relying on rote recall."
                ],
                "science": [
                    "Engage in active laboratory practice and online simulations to visualize core biological or physical systems.",
                    "Draft clean, labeled cell structures, circuit schematics, or flow diagrams to consolidate chemical dynamics.",
                    "Construct detailed concept maps connecting high-level theoretical laws to practical, observable experiments."
                ],
                "english": [
                    "Improve reading comprehension by actively reading scholarly publications and drafting critical 1-paragraph summaries.",
                    "Refine formal essay structures, practicing thesis formation, clear body mapping, and transition styling.",
                    "Enrich vocabulary and expression scales by researching and logging 10 advanced literary terms weekly."
                ],
                "computer_science": [
                    "Build consistent computer coding habits, building small console utilities to test core language features.",
                    "Solve basic algorithmic challenges on LeetCode or HackerRank to master control flows and loop efficiencies.",
                    "Develop simple portfolio projects (like a SQL contacts manager or local file parser) to synthesize syntax rules."
                ],
                "general": [
                    "Review all lecture slides and notes within 24 hours of presentation to maximize cognitive retention.",
                    "Initiate peer study circles to discuss difficult curriculum components and teach peer group members.",
                    "Design paper or digital flashcards for definitions, employing spaced repetition for memory enhancement."
                ]
            }
            
            # Analyze each course average
            for course_name, scores in course_scores.items():
                if not scores:
                    continue
                avg_score = sum(scores) / len(scores)
                
                # Check for average score below threshold of 70%
                if avg_score < 70.0:
                    c_lower = course_name.lower()
                    
                    # Map course names to respective curriculum tips
                    if "math" in c_lower:
                        selected_tips = tips_bank["math"]
                    elif "science" in c_lower:
                        selected_tips = tips_bank["science"]
                    elif "english" in c_lower:
                        selected_tips = tips_bank["english"]
                    elif "computer" in c_lower or "code" in c_lower or "programming" in c_lower:
                        selected_tips = tips_bank["computer_science"]
                    else:
                        selected_tips = tips_bank["general"]
                        
                    recommendations.append({
                        "subject": course_name,
                        "tips": selected_tips
                    })
                    
            return recommendations
            
        except Exception:
            return []
