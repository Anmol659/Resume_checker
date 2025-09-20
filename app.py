from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import your API router
from api.v1.routers import analysis

# Import your services for initialization
from services import llm_service, vector_service
from db import database, models

# Create the database tables if they don't exist
# This line will connect to your Supabase DB on startup
models.Base.metadata.create_all(bind=database.engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load AI models and connect to services on startup
    print("Application startup: Loading AI Models...")
    llm_service.load_model()
    vector_service.load_embedding_model()
    print("Application startup complete.")
    yield
    # Clean up resources on shutdown (optional)
    print("Application shutdown.")

app = FastAPI(
    lifespan=lifespan,
    title="Automated Resume Relevance Checker",
    description="An AI-powered system to analyze and score resumes against job descriptions.",
    version="1.0.0"
)

# Include your API router
app.include_router(analysis.router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "API is running."}

