from sentence_transformers import SentenceTransformer, util
import torch
from core import config

# Use a global variable to hold the model so it's loaded only once.
embedding_model = None

def load_embedding_model():
    """Loads the sentence-transformer model into memory."""
    global embedding_model
    if embedding_model is None:
        print("Loading the embedding model...")
        try:
            # Check if a CUDA GPU is available, otherwise use CPU
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            embedding_model = SentenceTransformer(config.EMBEDDING_MODEL_NAME, device=device)
            print(f"Embedding model loaded successfully on '{device}'.")
        except Exception as e:
            print(f"Error loading embedding model: {e}")

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculates the cosine similarity between two texts.
    Returns a score between 0 and 1.
    """
    if embedding_model is None:
        print("Error: Embedding model is not loaded.")
        return 0.0

    try:
        # Generate embeddings for both texts
        embedding1 = embedding_model.encode(text1, convert_to_tensor=True)
        embedding2 = embedding_model.encode(text2, convert_to_tensor=True)

        # Compute cosine-similarity
        cosine_scores = util.cos_sim(embedding1, embedding2)
        
        # The result is a tensor, get the float value from it
        similarity_score = cosine_scores.item()
        return similarity_score
        
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0

