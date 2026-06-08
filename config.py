import os
from dotenv import load_dotenv

load_dotenv()

# LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"

# Embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Paths
DOCUMENTS_PATH = "./documents"
CHROMA_PATH = "./chroma_db"
CHROMA_COLLECTION = "unofficial_guide"

# Retrieval
N_RESULTS = 3