from fastapi import APIRouter, UploadFile, File, HTTPException, status
import tempfile
import os
from .. import schemas
# --- This is the crucial import ---
from services import parser_service, analysis_service

router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"]
)

@router.post("/resume", response_model=schemas.AnalysisResult)
async def analyze_resume(
    job_description: UploadFile = File(..., description="The Job Description file (PDF or DOCX)."),
    resume: UploadFile = File(..., description="The Resume file (PDF or DOCX).")
):
    """
    Analyzes a resume against a job description and returns a relevance score and feedback.
    """
    # Use a temporary directory to safely handle file uploads
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # --- Save and process Job Description ---
            jd_path = os.path.join(temp_dir, job_description.filename)
            with open(jd_path, "wb") as f:
                f.write(await job_description.read())
            
            print(f"Parsing Job Description: {job_description.filename}")
            jd_text = parser_service.parse_document(jd_path)
            if not jd_text:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Could not parse the job description file: {job_description.filename}"
                )

            # --- Save and process Resume ---
            resume_path = os.path.join(temp_dir, resume.filename)
            with open(resume_path, "wb") as f:
                f.write(await resume.read())
            
            print(f"Parsing Resume: {resume.filename}")
            resume_text = parser_service.parse_document(resume_path)
            if not resume_text:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Could not parse the resume file: {resume.filename}"
                )

            # --- This is the key change: Call the REAL analysis service ---
            print("Handing off to analysis service...")
            result = analysis_service.analyze_resume(resume_text=resume_text, jd_text=jd_text)
            
            return result

        except HTTPException as e:
            # Re-raise HTTP exceptions to be handled by FastAPI
            raise e
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred during analysis: {str(e)}"
            )

