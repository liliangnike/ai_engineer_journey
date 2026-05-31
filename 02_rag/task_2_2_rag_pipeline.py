import chromadb
from openai import OpenAI
from sentence_transformers import SentenceTransformer

# Demo how to construct a complete RAG (Retrieval -> Augmented -> Generation)
# 1. Initialize Clients
client = OpenAI(base_url = "http://localhost:11434/v1", api_key = "ollama")
db_client = chromadb.PersistentClient(path="./vector_db")
collection = db_client.get_collection("company_knowledge")

# 2. Load Embedding Model (small, efficient, local)
model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_context(query_text):
    '''Retrieve relevant docs from vector DB.'''
    query_vector = model.encode(query_text).tolist()
    results = collection.query(query_embeddings = [query_vector], n_results = 2)
    return "\n".join(results['documents'][0])

def rag_pipeline(user_prompt):
    # 1. retrieve knowledge
    context = retrieve_context(user_prompt)

    # 2. Build augmented prompt
    prompt = f"You are a helpful assistant. Use the following context to answer the question. Context: {context} Question: {user_prompt}"

    # 3. Generate response via LLM
    response = client.chat.completions.create(model = "qwen2.5-coder:7b", messages = [{"role": "user", "content": prompt}])
    return response.choices[0].message.content

if __name__ == "__main__":
    question = "What is the status of Project-X-99?"
    answer = rag_pipeline(question)
    print(f"AI Response: {answer}")
