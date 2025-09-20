from pydantic import BaseModel
from typing import List, Optional

# Defines the structure for a single resume's analysis result.
class AnalysisResult(BaseModel):
    file_name: str
    relevance_score: int
    verdict: str
    missing_skills: List[str]
    feedback: str
    
    class Config:
        from_attributes = True

# Defines the overall response structure for a job description analysis.
class JobDescriptionAnalysis(BaseModel):
    # This new field will hold the ID of the document created in Firestore.
    # It's optional, so the API won't fail if the save operation doesn't return an ID.
    firestore_job_id: Optional[str] = None 
    
    job_description_file: str
    total_resumes_analyzed: int
    results: List[AnalysisResult]

    class Config:
        from_attributes = True

