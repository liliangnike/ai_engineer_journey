import chromadb
from openai import OpenAI
from sentence_transformers import SentenceTransformer

class RAGAgent:
    def __init__(self):
        self.client = OpenAI(base_url = "http://localhost:11434/v1", api_key = "ollama")
        self.db_client = chromadb.PersistentClient(path="./vector_db")
        self.collection = self.db_client.get_collection("company_knowledge")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def get_answer(self, user_prompt):
        query_vector = self.model.encode(user_prompt).tolist()
        results = self.collection.query(query_embeddings = [query_vector], n_results = 1, include = ['documents', 'distances'])
        if results['distances'][0][0] > 1.0:
            return "Sorry, I did not find any information about your question."

        context = "\n".join(results['documents'][0])

        system_instruction = "You are a helpful assistant. Use the following context to answer the user question. If the answer is not in the context, say you don't know."
        formatted_prompt = f"Context:\n{context}\n\nQuestion: {user_prompt}"
        response = self.client.chat.completions.create(
                    model = "qwen2.5-coder:7b", 
                    messages = [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": formatted_prompt}
                    ]
                )

        return response.choices[0].message.content

if __name__ == "__main__":
    agent = RAGAgent()
    print(agent.get_answer("What is Project-X-99?"))
