import chromadb
from sentence_transformers import SentenceTransformer

# 1. Initialize Vector Databse
client = chromadb.PersistentClient(path="./vector_db")
collection = client.create_collection("company_knowledge")

# 2. Load Embedding Model (small, efficient, local)
model = SentenceTransformer('all-MiniLM-L6-v2')

# 3. Prepare Private Knowledge
documents = [
    "Project-X-99 is the codename for our next-gen network switch.",
    "The 996 culture is strictly discouraged in our foreign-invested enterprise environment.",
    "TR-069 is a technical specification for remote management of end-user devices."
]

# 4. Embed and Store
for i, doc in enumerate(documents):
    vector = model.encode(doc).tolist()
    collection.add(ids = [str(i)], embeddings = [vector], documents = [doc])

# 5. Query function
def query_knowledge(query_text):
    query_vector = model.encode(query_text).tolist()
    result = collection.query(query_embeddings = [query_vector], n_results = 1)

    return result['documents'][0]

if __name__ == "__main__":
    answer = query_knowledge("What is Project-X-99?")
    print(f"Received context: {answer}")
