from pydantic import BaseModel, Field
from typing import List, Optional

class AnalysisResult(BaseModel):
    """Defines the structure for a single resume analysis result."""
    file_name: str = Field(..., description="The name of the resume file.")
    relevance_score: int = Field(..., ge=0, le=100, description="The final relevance score (0-100).")
    verdict: str = Field(..., description="The final verdict (e.g., 'High', 'Medium', 'Low').")
    missing_skills: List[str] = Field(..., description="A list of skills missing from the resume.")
    feedback: str = Field(..., description="Personalized feedback for the candidate.")

    class Config:
        # This allows the model to be created from ORM objects (like SQLAlchemy models)
        from_attributes = True

class JobDescriptionAnalysis(BaseModel):
    """Defines the structure for the full analysis of a job description."""
    job_description_file: str = Field(..., description="The name of the job description file.")
    total_resumes_analyzed: int = Field(..., description="Total number of resumes processed.")
    results: List[AnalysisResult] = Field(..., description="A list of analysis results for each resume.")
