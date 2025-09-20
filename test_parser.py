# test_parser.py
from services.parser_service import parse_document

if __name__ == "__main__":
    # Make sure the file path is correct
    resume_path = r"C:\Users\anmol\OneDrive\Desktop\Resume_checker\data\resumes\resume - 3.pdf"
    
    print(f"Attempting to parse: {resume_path}")
    
    extracted_text = parse_document(resume_path)
    
    if extracted_text:
        print("\n--- Successfully Extracted Text ---")
        print(extracted_text[:500]) # Print the first 500 characters
        print("\n---------------------------------")
    else:
        print("Failed to extract text.")