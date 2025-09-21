Automated Resume Relevance Checker - Backend
This repository contains the backend server for the Innomatics Resume Analyzer, an AI-powered system designed to automate the process of screening and scoring resumes against job descriptions.

The application is built with FastAPI and leverages a hybrid AI approach, combining semantic search for quantitative scoring and a powerful Large Language Model (Google's Gemini 1.5 Flash) for qualitative feedback.

✨ Features
FastAPI Backend: A modern, high-performance web framework for building APIs.

Document Parsing: Supports both PDF (.pdf) and Word (.docx) formats for resumes and job descriptions.

Hybrid AI Analysis:

Semantic Scoring: Uses sentence-transformers to generate embeddings and calculate a precise relevance score based on content similarity.

Keyword Analysis: Identifies key skills from the job description that are missing in the resume.

AI-Powered Feedback: Calls the Google Gemini 1.5 Flash API to generate detailed, structured feedback, including a summary, strengths, and areas for improvement.

Database Integration: Connects to a Supabase (PostgreSQL) database to persist all analysis results.

Asynchronous: Built with async and await to handle multiple requests efficiently.

🏛️ System Architecture
The backend follows a service-oriented architecture, separating concerns for clarity and scalability.

graph TD
    A[User via Frontend] -- File Uploads --> B(FastAPI Endpoint);
    B -- JD & Resume --> C{Analysis Service};
    C -- Text --> D[Parser Service];
    C -- Text --> E[Vector Service];
    E -- Similarity Score --> C;
    C -- Text --> F[LLM Service];
    F -- Gemini API Call --> G((Google Cloud));
    G -- Detailed Feedback --> F;
    F -- Feedback --> C;
    C -- Final Results --> H{DB Service};
    H -- Save Results --> I((Supabase DB));
    B -- Formatted Response --> A;

🛠️ Tech Stack
Framework: FastAPI

Language: Python 3.10+

Database: Supabase (PostgreSQL) with SQLAlchemy ORM

AI & Machine Learning:

LLM: Google Gemini 1.5 Flash API

Embeddings: sentence-transformers (all-MiniLM-L6-v2)

Document Parsing: PyMuPDF

API Client: httpx

🚀 Getting Started
Follow these instructions to set up and run the backend server on your local machine.

1. Prerequisites
Python 3.10 or higher

A Supabase project with a PostgreSQL database.

A Google AI Studio API key for Gemini.

2. Installation & Setup
a. Clone the repository:

git clone <your-repository-url>
cd <repository-folder>

b. Create a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

c. Install dependencies:

pip install -r requirements.txt

d. Configure Environment Variables:
The application requires a .env file in the root directory to store your secret keys. Create a file named .env and add the following, replacing the placeholders with your actual credentials:

# Your Supabase database connection string
DATABASE_URL="postgresql://postgres:[YOUR-SUPABASE-PASSWORD]@db.rtzyysbxbasrslaaoagc.supabase.co:5432/postgres"

# Your Google AI Studio API key
GEMINI_API_KEY="AIzaSy...YourActualKey"

(Note: The current database.py and llm_service.py scripts are hardcoded. For local development, you can edit them directly. The .env approach is recommended for production.)

3. Running the Server
Once the setup is complete, you can start the development server using Uvicorn:

uvicorn app:app --reload

The server will be running at http://127.0.0.1:8000.

📖 API Documentation
The API is self-documenting thanks to FastAPI. Once the server is running, you can access the interactive Swagger UI to test the endpoints:

Swagger UI: http://127.0.0.1:8000/docs

Main Endpoint: POST /api/v1/resume
This is the primary endpoint for analyzing resumes.

Request Body: multipart/form-data

job_description: The job description file (.pdf, .docx).

resumes: One or more resume files (.pdf, .docx).

Success Response (200 OK):
The API returns a detailed JSON object with the analysis results for each resume.

{
  "job_description_file": "sample_jd.pdf",
  "total_resumes_analyzed": 1,
  "results": [
    {
      "file_name": "candidate_resume.pdf",
      "relevance_score": 82,
      "verdict": "High",
      "missing_skills": ["kafka", "c++"],
      "feedback": {
        "summary": "The candidate is a strong fit for the Data Science Intern role...",
        "strengths": [
          "Proficient in Python, SQL, and data visualization tools like Power BI.",
          "Hands-on project experience with EDA and web scraping is highly relevant."
        ],
        "improvements": [
          "The resume lacks experience with large-scale data processing tools like Spark.",
          "Adding experience with data pipeline tools like Kafka would strengthen the application."
        ]
      }
    }
  ],
  "firestore_job_id": "job_abc123"
}

📁 Project Structure
/resume-checker-backend/
├── api/                  # FastAPI routers and schemas
│   └── v1/
│       ├── routers/
│       │   └── analysis.py   # Main API endpoint logic
│       └── schemas.py      # Pydantic data models
├── db/                     # Database connection and table models
│   ├── database.py
│   └── models.py
├── services/               # Core application logic
│   ├── analysis_service.py # Orchestrates the AI pipeline
│   ├── db_service.py       # Handles database operations
│   ├── llm_service.py      # Connects to the Gemini API
│   ├── parser_service.py   # Extracts text from documents
│   └── vector_service.py   # Generates embeddings and similarity scores
├── app.py                  # Main FastAPI application entry point
├── requirements.txt      # Python dependencies
└── ...
