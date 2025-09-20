import torch
from transformers import pipeline
import json

# --- Global variable to hold the loaded model ---
llm_pipeline = None

def load_model():
    """
    Loads the Phi-3 model pipeline. This is done once when the app starts.
    """
    global llm_pipeline
    if llm_pipeline is None:
        print("Loading the LLM model for the first time...")
        # Using device_map="auto" will automatically use a GPU if available
        llm_pipeline = pipeline(
            "text-generation",
            model="microsoft/Phi-3-mini-4k-instruct",
            device_map="auto",
            torch_dtype="auto",
            trust_remote_code=True,
            # For memory optimization on smaller hardware
            model_kwargs={"load_in_8bit": True} 
        )
        print("LLM Model loaded successfully.")

def generate_analysis(resume_text: str, jd_text: str) -> dict:
    """
    Generates an analysis of the resume against the job description using the LLM.
    """
    if llm_pipeline is None:
        raise RuntimeError("LLM model is not loaded. Please call load_model() first.")

    # This is our instruction (prompt) to the LLM.
    # We are asking it to act as an expert recruiter and return a JSON object.
    messages = [
        {
            "role": "system",
            "content": """You are an expert technical recruiter and resume screening assistant. 
            Your task is to analyze a resume against a job description.
            Evaluate the resume based on the requirements in the job description and provide a structured JSON output.
            The JSON object should have the following keys:
            - "relevance_score": An integer score from 0 to 100 representing how well the resume matches the job description. 100 is a perfect match.
            - "missing_skills": A list of key skills or technologies mentioned in the job description that are missing from the resume.
            - "feedback": A concise, one-paragraph feedback for the candidate, highlighting their strengths and areas for improvement based on the job description.
            """
        },
        {
            "role": "user",
            "content": f"""
            Here is the Job Description:
            ---
            {jd_text}
            ---

            Here is the Resume:
            ---
            {resume_text}
            ---
            """
        }
    ]

    prompt = llm_pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # We set max_new_tokens to ensure the model has enough space to generate the full JSON
    outputs = llm_pipeline(prompt, max_new_tokens=1024, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    
    generated_text = outputs[0]["generated_text"]
    
    # --- Extract JSON from the model's response ---
    # The model's output includes the prompt, so we need to find the JSON part.
    try:
        json_str_start = generated_text.find('{"relevance_score"')
        if json_str_start == -1:
             json_str_start = generated_text.find('{')

        json_str_end = generated_text.rfind('}') + 1
        
        if json_str_start != -1:
            json_response = generated_text[json_str_start:json_str_end]
            return json.loads(json_response)
        else:
            raise ValueError("Could not find JSON object in the LLM response.")
            
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing LLM response: {e}")
        print(f"Raw Response: {generated_text}")
        # Return a default error structure if parsing fails
        return {
            "relevance_score": 0,
            "missing_skills": ["Error processing response"],
            "feedback": "Could not generate analysis due to an internal error."
        }
