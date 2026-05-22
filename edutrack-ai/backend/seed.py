import datetime
import random
from sqlalchemy.orm import Session

from backend.database import engine, Base, SessionLocal
from backend.models import User, Student, Teacher, Course, Grade, Attendance
from backend.auth import get_password_hash
from backend.routes.grades import calculate_letter_grade

def seed_db():
    # Make sure all tables are created
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("🌱 Seeding database...")
        
        # 1. Seed System Users (Admin and default Teachers/Students if desired)
        # Requirement: Admin user (admin@edutrack.com / Admin123!)
        # Requirement: Teacher user (ramesh@edutrack.com / Teacher123!)
        system_users = [
            {"email": "admin@edutrack.com", "password": "Admin123!", "role": "admin"},
            {"email": "ramesh@edutrack.com", "password": "Teacher123!", "role": "teacher"},
            {"email": "lakshmi@edutrack.com", "password": "Teacher123!", "role": "teacher"},
            {"email": "venkat@edutrack.com", "password": "Teacher123!", "role": "teacher"},
            {"email": "arjun@edutrack.com", "password": "Student123!", "role": "student"},
            {"email": "priya@edutrack.com", "password": "Student123!", "role": "student"},
            {"email": "ravi@edutrack.com", "password": "Student123!", "role": "student"},
            {"email": "sneha@edutrack.com", "password": "Student123!", "role": "student"},
            {"email": "amit@edutrack.com", "password": "Student123!", "role": "student"}
        ]
        
        user_map = {}
        for user_info in system_users:
            existing_user = db.query(User).filter(User.email == user_info["email"]).first()
            if not existing_user:
                print(f"Creating user: {user_info['email']}")
                hashed_pw = get_password_hash(user_info["password"])
                new_user = User(
                    email=user_info["email"],
                    password_hash=hashed_pw,
                    role=user_info["role"]
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                user_map[user_info["email"]] = new_user
            else:
                user_map[user_info["email"]] = existing_user

        # 2. Seed Teachers
        # Requirement: Ramesh, Lakshmi, Venkat
        teachers_data = [
            {"name": "Mr. Ramesh", "email": "ramesh@edutrack.com", "subject": "Math"},
            {"name": "Mrs. Lakshmi", "email": "lakshmi@edutrack.com", "subject": "Science"},
            {"name": "Mr. Venkat", "email": "venkat@edutrack.com", "subject": "English"}
        ]
        
        teacher_map = {}
        for t_info in teachers_data:
            existing_teacher = db.query(Teacher).filter(Teacher.email == t_info["email"]).first()
            if not existing_teacher:
                print(f"Creating teacher: {t_info['name']}")
                hashed_pw = get_password_hash("Teacher123!")
                new_teacher = Teacher(
                    name=t_info["name"],
                    email=t_info["email"],
                    subject=t_info["subject"],
                    password_hash=hashed_pw
                )
                db.add(new_teacher)
                db.commit()
                db.refresh(new_teacher)
                teacher_map[t_info["email"]] = new_teacher
            else:
                teacher_map[t_info["email"]] = existing_teacher

        # 3. Seed Students
        # Requirement: Arjun Sharma, Priya Patel, Ravi Kumar, Sneha Reddy, Amit Singh
        students_data = [
            {"name": "Arjun Sharma", "email": "arjun@edutrack.com", "grade_level": "Grade 10"},
            {"name": "Priya Patel", "email": "priya@edutrack.com", "grade_level": "Grade 11"},
            {"name": "Ravi Kumar", "email": "ravi@edutrack.com", "grade_level": "Grade 10"},
            {"name": "Sneha Reddy", "email": "sneha@edutrack.com", "grade_level": "Grade 12"},
            {"name": "Amit Singh", "email": "amit@edutrack.com", "grade_level": "Grade 11"}
        ]
        
        student_map = {}
        for s_info in students_data:
            existing_student = db.query(Student).filter(Student.email == s_info["email"]).first()
            if not existing_student:
                print(f"Creating student: {s_info['name']}")
                new_student = Student(
                    name=s_info["name"],
                    email=s_info["email"],
                    grade_level=s_info["grade_level"]
                )
                db.add(new_student)
                db.commit()
                db.refresh(new_student)
                student_map[s_info["email"]] = new_student
            else:
                student_map[s_info["email"]] = existing_student

        # 4. Seed Courses
        # Requirement: Mathematics (teacher: Ramesh, credits: 4)
        # Requirement: Science (teacher: Lakshmi, credits: 4)
        # Requirement: English (teacher: Venkat, credits: 3)
        # Requirement: Computer Science (teacher: Ramesh, credits: 3)
        courses_data = [
            {"name": "Mathematics", "teacher_email": "ramesh@edutrack.com", "schedule": "Mon/Wed 9:00 AM", "credits": 4},
            {"name": "Science", "teacher_email": "lakshmi@edutrack.com", "schedule": "Tue/Thu 10:30 AM", "credits": 4},
            {"name": "English", "teacher_email": "venkat@edutrack.com", "schedule": "Mon/Wed 1:00 PM", "credits": 3},
            {"name": "Computer Science", "teacher_email": "ramesh@edutrack.com", "schedule": "Fri 11:00 AM", "credits": 3}
        ]
        
        course_map = {}
        for c_info in courses_data:
            existing_course = db.query(Course).filter(Course.name == c_info["name"]).first()
            if not existing_course:
                print(f"Creating course: {c_info['name']}")
                teacher = teacher_map.get(c_info["teacher_email"])
                new_course = Course(
                    name=c_info["name"],
                    teacher_id=teacher.id if teacher else None,
                    schedule=c_info["schedule"],
                    credits=c_info["credits"]
                )
                db.add(new_course)
                db.commit()
                db.refresh(new_course)
                course_map[c_info["name"]] = new_course
            else:
                course_map[c_info["name"]] = existing_course

        # 5. Seed Grades (Generate realistic grades for the past 3 months)
        # Arjun: mostly 85-95 (good student)
        # Priya: mostly 70-80 (average)
        # Ravi: mostly 45-60 (at-risk student)
        # Sneha: mostly 90-100 (excellent)
        # Amit: mostly 55-70 (below average)
        grade_profiles = {
            "arjun@edutrack.com": (85, 96),
            "priya@edutrack.com": (70, 81),
            "ravi@edutrack.com": (45, 61),
            "sneha@edutrack.com": (90, 100),
            "amit@edutrack.com": (55, 71)
        }
        
        # 3 exams spaced over the past 3 months
        base_date = datetime.datetime.utcnow() - datetime.timedelta(days=90)
        exam_offsets = [15, 45, 75]  # days from base_date
        
        for email, (low, high) in grade_profiles.items():
            student = student_map.get(email)
            if not student:
                continue
                
            # Check if this student already has grades
            has_grades = db.query(Grade).filter(Grade.student_id == student.id).first()
            if has_grades:
                print(f"Grades already exist for student: {student.name}. Skipping grade seed.")
                continue
                
            for c_name, course in course_map.items():
                for idx, offset in enumerate(exam_offsets):
                    score = float(random.randint(low, high))
                    letter = calculate_letter_grade(score)
                    exam_date = base_date + datetime.timedelta(days=offset)
                    
                    new_grade = Grade(
                        student_id=student.id,
                        course_id=course.id,
                        score=score,
                        letter_grade=letter,
                        date=exam_date
                    )
                    db.add(new_grade)
        db.commit()
        print("✅ Grades seeding complete.")

        # 6. Seed Attendance (Generate attendance for past 30 days)
        # Arjun: 90% present
        # Priya: 80% present
        # Ravi: 60% present (at-risk)
        # Sneha: 95% present
        # Amit: 70% present
        attendance_profiles = {
            "arjun@edutrack.com": 0.90,
            "priya@edutrack.com": 0.80,
            "ravi@edutrack.com": 0.60,
            "sneha@edutrack.com": 0.95,
            "amit@edutrack.com": 0.70
        }
        
        # Past 30 days (excluding weekends)
        today = datetime.datetime.utcnow()
        for email, present_pct in attendance_profiles.items():
            student = student_map.get(email)
            if not student:
                continue
                
            # Check if student already has attendance
            has_attendance = db.query(Attendance).filter(Attendance.student_id == student.id).first()
            if has_attendance:
                print(f"Attendance already exists for student: {student.name}. Skipping attendance seed.")
                continue
                
            for c_name, course in course_map.items():
                for day in range(30):
                    rec_date = today - datetime.timedelta(days=day)
                    # Skip weekends
                    if rec_date.weekday() >= 5:
                        continue
                        
                    # Decide attendance status based on percentage profile
                    rand_val = random.random()
                    if rand_val <= present_pct:
                        # Mostly present, occasionally late
                        status = "present" if random.random() > 0.05 else "late"
                    else:
                        status = "absent"
                        
                    new_attendance = Attendance(
                        student_id=student.id,
                        course_id=course.id,
                        date=rec_date,
                        status=status
                    )
                    db.add(new_attendance)
        db.commit()
        print("✅ Attendance seeding complete.")
        
        print("🎉 Database successfully seeded!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error during database seeding: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
