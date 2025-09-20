from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    content = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # This creates a relationship so you can access all results for a JD
    results = relationship("AnalysisResult", back_populates="job_description", cascade="all, delete-orphan")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"))
    
    file_name = Column(String)
    relevance_score = Column(Integer)
    verdict = Column(String)
    missing_skills = Column(ARRAY(String))
    feedback = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # This links the result back to its parent JobDescription
    job_description = relationship("JobDescription", back_populates="results")

