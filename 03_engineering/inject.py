import os
import chromadb
from sentence_transformers import SentenceTransformer
from config import Config

def inject_new_knowledge(doc_id: str, document_text: str):
    """
    Independent knowledge injection function to append content to the vector database.
    """
    print(f"Initializing embedding model: {Config.EMBEDDING_MODEL}...")
    model = SentenceTransformer(Config.EMBEDDING_MODEL)
    
    print(f"Connecting to persistent vector DB: {Config.VECTOR_DB_PATH}...")
    db_client = chromadb.PersistentClient(path=Config.VECTOR_DB_PATH)
    
    # Get or create the collection based on configuration
    collection = db_client.get_or_create_collection(Config.COLLECTION_NAME)
    
    # 1. Compute text embeddings
    print("Computing text embeddings...")
    vector = model.encode(document_text).tolist()
    
    # 2. Write data into ChromaDB
    print(f"Writing knowledge with ID [{doc_id}] into collection...")
    collection.add(
        embeddings=[vector],
        documents=[document_text],
        ids=[doc_id]
    )
    print("Data injection completed successfully!")

if __name__ == "__main__":
    # Test case to ingest a new piece of project knowledge
    test_id = "project_y_100"
    test_text = "Project-Y-100 is an automated script framework for TR-143 speed test verification, fully compatible with DHCPv6 environment."
    
    inject_new_knowledge(test_id, test_text)
