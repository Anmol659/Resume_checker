from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.v1.routers import analysis
from services import llm_service

# The lifespan manager correctly loads the model on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: Loading AI Model...")
    llm_service.load_model()
    yield
    print("Application shutdown.")

app = FastAPI(
    title="Automated Resume Relevance Checker",
    description="An AI-powered system to analyze and score resumes against job descriptions.",
    version="1.0.0",
    lifespan=lifespan  # This line tells FastAPI to use the lifespan manager
)

# Include the API router
app.include_router(analysis.router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
def read_root():
    """A simple health check endpoint to confirm the API is running."""
    return {"status": "API is running!"}

