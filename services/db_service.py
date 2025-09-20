from sqlalchemy.orm import Session
from db import models

def save_analysis_to_db(
    db: Session,
    jd_filename: str,
    jd_content: str,
    results: list
):
    """
    Saves the job description and all analysis results to the database.
    """
    try:
        # Create a new JobDescription record
        db_jd = models.JobDescription(
            file_name=jd_filename,
            content=jd_content
        )
        db.add(db_jd)
        db.commit()
        db.refresh(db_jd)

        # For each result, create a new AnalysisResult record linked to the JD
        for result in results:
            db_result = models.AnalysisResult(
                job_description_id=db_jd.id,
                file_name=result["file_name"],
                relevance_score=result["relevance_score"],
                verdict=result["verdict"],
                missing_skills=result["missing_skills"],
                feedback=result["feedback"]
            )
            db.add(db_result)
        
        db.commit()
        return db_jd.id
    except Exception as e:
        db.rollback()
        print(f"Error saving to database: {e}")
        return None

