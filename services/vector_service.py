from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Tuple

# --- Global variable to hold the loaded embedding model ---
embedding_model = None

def load_embedding_model():
    """Loads the sentence-transformer model once."""
    global embedding_model
    if embedding_model is None:
        print("Loading the embedding model for the first time...")
        # We are using a predefined, efficient model for creating embeddings.
        # This model is great for semantic similarity tasks.
        model_name = "all-MiniLM-L6-v2" 
        embedding_model = SentenceTransformer(model_name)
        print("Embedding model loaded successfully.")

def create_embeddings(texts: List[str]) -> np.ndarray:
    """
    Creates numerical vector representations (embeddings) for a list of texts.
    """
    if embedding_model is None:
        raise RuntimeError("Embedding model is not loaded. Please call load_embedding_model() first.")
    
    # The .encode() method converts text into high-dimensional vectors.
    embeddings = embedding_model.encode(texts, convert_to_tensor=False)
    return np.array(embeddings).astype('float32')

def get_semantic_similarity(resume_embedding: np.ndarray, jd_embedding: np.ndarray) -> float:
    """
    Calculates the cosine similarity between two embeddings and scales it to a 0-100 score.
    """
    # FAISS uses IndexFlatIP (Inner Product) for cosine similarity. 
    # For normalized vectors, Inner Product is equivalent to Cosine Similarity.
    
    # Reshape for FAISS, which expects 2D arrays
    resume_emb = np.reshape(resume_embedding, (1, -1))
    jd_emb = np.reshape(jd_embedding, (1, -1))
    
    # Normalize the embeddings to unit vectors for accurate cosine similarity
    faiss.normalize_L2(resume_emb)
    faiss.normalize_L2(jd_emb)
    
    # Create a FAISS index for the job description embedding
    index = faiss.IndexFlatIP(jd_emb.shape[1])
    index.add(jd_emb)
    
    # Search for the resume embedding within the JD index
    # We are looking for the 1 nearest neighbor
    distances, _ = index.search(resume_emb, 1)
    
    # The distance is the cosine similarity. It's between -1 and 1.
    # We scale it to be between 0 and 100 for our scoring.
    similarity = distances[0][0]
    scaled_score = max(0, min(100, (similarity + 1) / 2 * 100))
    
    return scaled_score
