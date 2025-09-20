import logging
from typing import Dict, Any, IO
from . import parser_service, vector_service, llm_service

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def perform_hybrid_analysis(resume_file: IO[bytes], jd_file: IO[bytes]) -> Dict[str, Any]:
    """
    Orchestrates the new hybrid analysis pipeline.
    """
    logger.info(f"--- Starting Hybrid Analysis for: {resume_file.filename} ---")

    await resume_file.seek(0)
    await jd_file.seek(0)
    
    logger.info("Parsing document contents...")
    resume_text = await parser_service.parse_document(resume_file, resume_file.filename)
    jd_text = await parser_service.parse_document(jd_file, jd_file.filename)

    if not resume_text or not jd_text:
        return {
            "file_name": resume_file.filename,
            "relevance_score": 0,
            "verdict": "Error",
            "missing_skills": [],
            "feedback": "Could not parse one or both documents."
        }

    logger.info("Step 1: Getting semantic similarity score...")
    semantic_score = vector_service.calculate_similarity(resume_text, jd_text)
    
    logger.info("Step 2: Identifying missing skills via keyword search...")
    jd_skills = {"python", "spark", "sql", "data pipelines", "kafka", "c++", "mechanical", "manufacturing"} 
    missing_skills = sorted([skill for skill in jd_skills if skill not in resume_text.lower()])

    logger.info("Step 3: Getting qualitative feedback from LLM...")
    # CORRECTED: Changed ll_service to llm_service
    llm_feedback = await llm_service.get_llm_feedback(resume_text, jd_text)

    final_score = int(semantic_score * 100)
    verdict = "Low"
    if final_score >= 75:
        verdict = "High"
    elif final_score >= 50:
        verdict = "Medium"
        
    logger.info(f"--- Analysis Complete for: {resume_file.filename} | Score: {final_score} ---")

    return {
        "file_name": resume_file.filename,
        "relevance_score": final_score,
        "verdict": verdict,
        "missing_skills": missing_skills,
        "feedback": llm_feedback
    }

