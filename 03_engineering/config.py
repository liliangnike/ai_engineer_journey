import os

class Config:
    LLM_MODEL = "qwen2.5-coder:7b"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    VECTOR_DB_PATH = "./vector_db"
    COLLECTION_NAME = "company_knowledge"
    OLLAMA_URL = "http://localhost:11434/v1"
