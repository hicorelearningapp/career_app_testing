# single_file_profile_app.py
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os, shutil, time
from typing import Optional

# ---------------- Database Setup ----------------
DATABASE_URL = "sqlite:///./profile.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ---------------- Upload Directory ----------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- Models ----------------
class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mobile_number = Column(String, nullable=True)
    professional_title = Column(String, nullable=True)
    location = Column(String, nullable=True)
    professional_bio = Column(Text, nullable=True)
    job_alerts = Column(Boolean, default=False)
    linkedin_profile = Column(String, nullable=True)
    portfolio_website = Column(String, nullable=True)
    github_profile = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)
    job_titles = Column(String, nullable=True)
    work_type = Column(String, nullable=True)
    current_salary = Column(String, nullable=True)
    expected_salary = Column(String, nullable=True)
    availability_start = Column(String, nullable=True)
    relocate = Column(Boolean, default=False)
    remote = Column(Boolean, default=False)
    hybrid = Column(Boolean, default=False)
    company_name = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    job_location = Column(String, nullable=True)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    currently_working = Column(Boolean, default=False)
    responsibilities = Column(Text, nullable=True)
    skills = Column(String, nullable=True)
    education_level = Column(String, nullable=True)
    field_of_study = Column(String, nullable=True)
    college_name = Column(String, nullable=True)
    edu_start_year = Column(String, nullable=True)
    edu_end_year = Column(String, nullable=True)
    currently_studying = Column(Boolean, default=False)
    resume_skills = Column(String, nullable=True)
    resume_file = Column(String, nullable=True)
    certificate_name = Column(String, nullable=True)
    issuing_org = Column(String, nullable=True)
    issue_date = Column(String, nullable=True)
    expiry_date = Column(String, nullable=True)
    credential_url = Column(String, nullable=True)
    project_name = Column(String, nullable=True)
    technologies = Column(String, nullable=True)
    project_description = Column(Text, nullable=True)
    project_link = Column(String, nullable=True)
    project_image_url = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

# ---------------- App Setup ----------------
app = FastAPI()

# Allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Helpers ----------------
def save_file(file: UploadFile) -> str:
    filename = f"{int(time.time())}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path

def to_dict(model):
    """Convert SQLAlchemy model to dict (safe for JSON)."""
    return {k: v for k, v in model.__dict__.items() if k != "_sa_instance_state"}

# ---------------- CRUD Endpoints ----------------
@app.post("/profiles")
async def create_profile(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    mobile_number: Optional[str] = Form(None),
    professional_title: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    professional_bio: Optional[str] = Form(None),
    job_alerts: Optional[bool] = Form(False),
    linkedin_profile: Optional[str] = Form(None),
    portfolio_website: Optional[str] = Form(None),
    github_profile: Optional[str] = Form(None),
    job_titles: Optional[str] = Form(None),  # Comma-separated
    work_type: Optional[str] = Form(None),
    current_salary: Optional[str] = Form(None),
    expected_salary: Optional[str] = Form(None),
    availability_start: Optional[str] = Form(None),
    relocate: Optional[bool] = Form(False),
    remote: Optional[bool] = Form(False),
    hybrid: Optional[bool] = Form(False),
    company_name: Optional[str] = Form(None),
    job_title: Optional[str] = Form(None),
    job_location: Optional[str] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    currently_working: Optional[bool] = Form(False),
    responsibilities: Optional[str] = Form(None),
    skills: Optional[str] = Form(None),  # Comma-separated
    education_level: Optional[str] = Form(None),
    field_of_study: Optional[str] = Form(None),
    college_name: Optional[str] = Form(None),
    edu_start_year: Optional[str] = Form(None),
    edu_end_year: Optional[str] = Form(None),
    currently_studying: Optional[bool] = Form(False),
    resume_skills: Optional[str] = Form(None),  # Comma-separated
    resume_file: Optional[UploadFile] = File(None),
    certificate_name: Optional[str] = Form(None),
    issuing_org: Optional[str] = Form(None),
    issue_date: Optional[str] = Form(None),
    expiry_date: Optional[str] = Form(None),
    credential_url: Optional[str] = Form(None),
    project_name: Optional[str] = Form(None),
    technologies: Optional[str] = Form(None),  # Comma-separated
    project_description: Optional[str] = Form(None),
    project_link: Optional[str] = Form(None),
    project_image: Optional[UploadFile] = File(None),
    profile_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Save files if uploaded
    profile_image_path = save_file(profile_image) if profile_image else None
    resume_file_path = save_file(resume_file) if resume_file else None
    project_image_path = save_file(project_image) if project_image else None

    profile = Profile(
        first_name=first_name,
        last_name=last_name,
        email=email,
        mobile_number=mobile_number,
        professional_title=professional_title,
        location=location,
        professional_bio=professional_bio,
        job_alerts=job_alerts,
        linkedin_profile=linkedin_profile,
        portfolio_website=portfolio_website,
        github_profile=github_profile,
        profile_image=profile_image_path,
        job_titles=job_titles,
        work_type=work_type,
        current_salary=current_salary,
        expected_salary=expected_salary,
        availability_start=availability_start,
        relocate=relocate,
        remote=remote,
        hybrid=hybrid,
        company_name=company_name,
        job_title=job_title,
        job_location=job_location,
        start_date=start_date,
        end_date=end_date,
        currently_working=currently_working,
        responsibilities=responsibilities,
        skills=skills,
        education_level=education_level,
        field_of_study=field_of_study,
        college_name=college_name,
        edu_start_year=edu_start_year,
        edu_end_year=edu_end_year,
        currently_studying=currently_studying,
        resume_skills=resume_skills,
        resume_file=resume_file_path,
        certificate_name=certificate_name,
        issuing_org=issuing_org,
        issue_date=issue_date,
        expiry_date=expiry_date,
        credential_url=credential_url,
        project_name=project_name,
        technologies=technologies,
        project_description=project_description,
        project_link=project_link,
        project_image_url=project_image_path
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return to_dict(profile)

@app.get("/profiles")
def list_profiles(db: Session = Depends(get_db)):
    profiles = db.query(Profile).all()
    return [to_dict(p) for p in profiles]

@app.get("/profiles/{profile_id}")
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return to_dict(profile)

@app.put("/profiles/{profile_id}")
def update_profile(profile_id: int, first_name: str = Form(...), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile.first_name = first_name
    db.commit()
    db.refresh(profile)
    return to_dict(profile)

@app.delete("/profiles/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    db.delete(profile)
    db.commit()
    return {"detail": "Profile deleted successfully"}
