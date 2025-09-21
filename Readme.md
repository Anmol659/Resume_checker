# Automated Resume Relevance Checker - Backend  

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)  
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-brightgreen.svg)  
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-blue.svg)  
![LLM](https://img.shields.io/badge/LLM-Gemini%201.5%20Flash-orange.svg)  

This repository contains the backend server for the **Innomatics Resume Analyzer**, an AI-powered system designed to automate the process of screening and scoring resumes against job descriptions.  

The application is built with **FastAPI** and leverages a hybrid AI approach, combining semantic search for quantitative scoring and a powerful Large Language Model (**Google's Gemini 1.5 Flash**) for qualitative feedback.  

---

## ✨ Features  

- **FastAPI Backend**: A modern, high-performance web framework for building APIs.  
- **Document Parsing**: Supports both PDF (`.pdf`) and Word (`.docx`) formats for resumes and job descriptions.  
- **Hybrid AI Analysis**:
  - **Semantic Scoring**: Uses `sentence-transformers` to generate embeddings and calculate a precise relevance score based on content similarity.  
  - **Keyword Analysis**: Identifies key skills from the job description that are missing in the resume.  
  - **AI-Powered Feedback**: Calls the **Google Gemini 1.5 Flash API** to generate detailed, structured feedback, including a summary, strengths, and areas for improvement.  
- **Database Integration**: Connects to a **Supabase (PostgreSQL)** database to persist all analysis results.  
- **Asynchronous**: Built with `async` and `await` to handle multiple requests efficiently.  

---

## 🏛️ System Architecture  

```mermaid
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
