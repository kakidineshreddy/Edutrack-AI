from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, Base
from backend.auth import router as auth_router
from backend.routes.students import router as students_router
from backend.routes.teachers import router as teachers_router
from backend.routes.courses import router as courses_router
from backend.routes.grades import router as grades_router
from backend.routes.attendance import router as attendance_router
from backend.routes.analytics import router as analytics_router

# Initialize FastAPI application
app = FastAPI(
    title="EduTrack AI API",
    description="Production-ready student performance tracking backend with AI-driven analytics",
    version="1.0.0"
)

# Enable CORS for the local Live Server origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event handler to automatically create all relational database tables
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Include API Routers
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(teachers_router)
app.include_router(courses_router)
app.include_router(grades_router)
app.include_router(attendance_router)
app.include_router(analytics_router)

# Root status endpoint
@app.get("/")
def read_root():
    return {"message": "EduTrack AI API Running"}
