# EduTrack AI - Setup Guide

EduTrack AI is a production-ready student performance tracking system. The solution features a FastAPI + SQLAlchemy backend connected to a PostgreSQL database, an scikit-learn & numpy powered local Machine Learning analytics engine for predicting student grades and recommending customized study actions, and a premium dark-themed 3D glassmorphic frontend utilizing Three.js and Chart.js.

## Prerequisites
- Python 3.14 (or equivalent modern Python environment)
- PostgreSQL 16 (with a database named `edutrack_ai`)
- VS Code with Live Server extension (running default on port 5500)

## Setup Steps
1. Open PowerShell or command line.
2. Navigate to the backend directory:
   ```bash
   cd C:\edutrack-ai\backend
   ```
3. Install the required Python packages from the requirements list:
   ```bash
   pip install -r ..\requirements.txt
   ```
4. Seed the database with sample students, courses, grades, and attendance metrics:
   ```bash
   python seed.py
   ```
5. Spin up the FastAPI server via Uvicorn:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## Access
- **API Server Root**: http://127.0.0.1:8000
- **Interactive API Documentation (Swagger UI)**: http://127.0.0.1:8000/docs
- **Web Application Portal**: Open the file [frontend/index.html](file:///C:/edutrack-ai/frontend/index.html) with VS Code's Live Server (origin `http://127.0.0.1:5500`).

## Login Credentials
Use the default loaded profiles to test dashboard visual features, student directories, grade registers, attendance calendars, and AI analytics metrics:
- **Administrator Access**:
  - **Email**: `admin@edutrack.com`
  - **Password**: `Admin123!`
  - **Role**: `admin`
- **Teacher Access**:
  - **Email**: `ramesh@edutrack.com`
  - **Password**: `Teacher123!`
  - **Role**: `teacher`
