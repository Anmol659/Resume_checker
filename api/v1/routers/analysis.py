from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import List
import os
import shutil

# Assuming your services are in the 'services' directory at the project root
from services.parser_service import parse_document
from .. import schemas # Import schemas from the parent __init__.py

router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"]
)

# Define a temporary directory to store uploaded files
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@router.post("/resume", response_model=schemas.JobDescriptionAnalysis)
async def analyze_resume_against_jd(
    job_description: UploadFile = File(..., description="The Job Description (PDF or DOCX)."),
    resumes: List[UploadFile] = File(..., description="One or more resumes to analyze (PDF or DOCX).")
):
    """
    Analyzes one or more resumes against a single job description.

    This is a dummy endpoint that demonstrates the API flow. It parses the files
    and returns a mock analysis result.
    """
    # --- 1. Process Job Description ---
    jd_path = os.path.join(TEMP_DIR, job_description.filename)
    with open(jd_path, "wb") as buffer:
        shutil.copyfileobj(job_description.file, buffer)

    jd_text = parse_document(jd_path)
    if not jd_text:
        raise HTTPException(status_code=400, detail=f"Could not parse job description: {job_description.filename}")

    # --- 2. Process Resumes ---
    analysis_results = []
    for resume in resumes:
        resume_path = os.path.join(TEMP_DIR, resume.filename)
        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        resume_text = parse_document(resume_path)
        if resume_text:
            # TODO: Replace this with the actual AI analysis logic in the next step
            # For now, we return a hardcoded "dummy" result.
            dummy_result = schemas.AnalysisResult(
                file_name=resume.filename,
                relevance_score=75,
                verdict="Medium",
                missing_skills=["Spark", "Advanced CI/CD"],
                feedback="Candidate shows strong potential in data engineering but lacks specific experience in large-scale data streaming with Spark."
            )
            analysis_results.append(dummy_result)

    # Clean up the temporary files
    shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)

    if not analysis_results:
        raise HTTPException(status_code=400, detail="No resumes could be parsed successfully.")

    return schemas.JobDescriptionAnalysis(
        job_description_file=job_description.filename,
        total_resumes_analyzed=len(analysis_results),
        results=analysis_results
    )
