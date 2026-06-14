import logging
import chromadb
from openai import OpenAI
from sentence_transformers import SentenceTransformer

logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s - %(levelname)s - %(message)s',
        filename = 'agent.log',
        filemode = 'a'
)

class RAGAgent:
    def __init__(self):
        self.client = OpenAI(base_url = "http://localhost:11434/v1", api_key = "ollama")
        self.db_client = chromadb.PersistentClient(path="./vector_db")
        self.collection = self.db_client.get_collection("company_knowledge")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chat_history: list[dict[str, str]]= []

    def get_answer(self, user_prompt):
        try:
            logging.info(f"User query: {user_prompt}")
            query_vector = self.model.encode(user_prompt).tolist()
            results = self.collection.query(query_embeddings = [query_vector], n_results = 1, include = ['documents', 'distances'])
            distance = results['distances'][0][0]
            if distance > 1.0:
                logging.warning(f"Blocked query (dist: {distance:.2f}): {user_prompt}")
                return "Sorry, I did not find any information about your question."

            logging.info(f"Answered query with distance: {distance:.2f}")
            context = "\n".join(results['documents'][0])

            self.chat_history.append({"role": "user", "content": user_prompt})
            # Only save the latest 3 history entries
            history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.chat_history[-3:]])

            system_instruction = "You are a helpful assistant. Use the following context to answer the user question. If the answer is not in the context, say you don't know."
            formatted_prompt = f"Context:\n{context}\n\nQuestion: {user_prompt}"
            response = self.client.chat.completions.create(
                    model = "qwen2.5-coder:7b", 
                    messages = [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": formatted_prompt}
                    ]
                )

            answer = response.choices[0].message.content

            # save answer
            self.chat_history.append({"role": "assistant", "content": answer})

            return answer
        except Exception as err:
            logging.error(f"Error occurred: {str(e)}")
            raise err

if __name__ == "__main__":
    agent = RAGAgent()
    print(agent.get_answer("What is Project-X-99?"))
