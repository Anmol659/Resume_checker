from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
import traceback
from sqlalchemy.orm import Session

# Import schemas and services
from .. import schemas 
from services import analysis_service, db_service, parser_service
from db.database import get_db

# The prefix is removed from here to prevent duplication
router = APIRouter(
    tags=["Analysis"]
)

# The path is now explicitly defined in the endpoint decorator
@router.post("/resume", response_model=schemas.JobDescriptionAnalysis)
async def analyze_resume_against_jd(
    job_description: UploadFile = File(..., description="The Job Description (PDF or DOCX)."),
    resumes: List[UploadFile] = File(..., description="One or more resumes to analyze (PDF or DOCX)."),
    db: Session = Depends(get_db) # Dependency injection for the DB session
):
    """
    Analyzes resumes against a job description and saves the results to Supabase.
    """
    analysis_results_for_db = []
    response_results = []
    db_job_id = None

    try:
        print("--- Analysis endpoint started ---")
        # --- 1. Process each resume ---
        print(f"Analyzing {len(resumes)} resume(s)...")
        for i, resume_file in enumerate(resumes):
            print(f"Processing resume {i+1}: {resume_file.filename}")
            await job_description.seek(0)
            ai_result = await analysis_service.perform_hybrid_analysis(resume_file, job_description)
            response_results.append(schemas.AnalysisResult(**ai_result))
            analysis_results_for_db.append(ai_result)
            print(f"Finished processing resume {i+1}.")

        if not response_results:
            raise HTTPException(status_code=400, detail="No resumes could be analyzed.")

        # --- 2. Save results to Supabase ---
        print("Parsing Job Description for database storage...")
        await job_description.seek(0)
        jd_text = await parser_service.parse_document(job_description, job_description.filename)
        if jd_text:
            print("Saving results to Supabase...")
            db_job_id = db_service.save_analysis_to_db(
                db=db,
                jd_filename=job_description.filename,
                jd_content=jd_text,
                results=analysis_results_for_db
            )
            print(f"Analysis successfully saved to Supabase under Job ID: {db_job_id}")
        else:
            print("Could not parse JD content, skipping save to DB.")

        # --- 3. Final API response ---
        print("--- Analysis endpoint finished successfully ---")
        return schemas.JobDescriptionAnalysis(
            # Using the ID from the database
            firestore_job_id=str(db_job_id) if db_job_id else None,
            job_description_file=job_description.filename,
            total_resumes_analyzed=len(response_results),
            results=response_results
        )

    except Exception as e:
        # This will now print the full, detailed error to your terminal
        print("!!! UNEXPECTED ERROR IN API ENDPOINT !!!")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred: {str(e)}")


@router.get("/health", tags=["Health Check"])
async def health_check():
    """
    Simple health check endpoint to confirm the API is running.
    """
    return {"status": "ok"}

