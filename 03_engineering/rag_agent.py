import logging
import chromadb
from config import Config
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
        self.client = OpenAI(base_url = Config.OLLAMA_URL, api_key = "ollama")
        self.db_client = chromadb.PersistentClient(path=Config.VECTOR_DB_PATH)
        self.collection = self.db_client.get_collection(Config.COLLECTION_NAME)
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
        self.chat_history: list[dict[str, str]]= []

    def get_answer(self, user_prompt):
        try:
            context = None
            logging.info(f"User query: {user_prompt}")
            query_vector = self.model.encode(user_prompt).tolist()
            results = self.collection.query(query_embeddings = [query_vector], n_results = 1, include = ['documents', 'distances'])

            distance = results['distances'][0][0]
            if distance > 1.0:
                context = "No relevant document found in database"
                logging.warning(f"Database query missed (dist: {distance:.2f}), relying on history.")
            else:
                context = "\n".join(results['documents'][0])
                logging.info(f"Answered query with distance: {distance:.2f}")

            self.chat_history.append({"role": "user", "content": user_prompt})
            # Only save the latest 3 history entries
            history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.chat_history[-3:]])

            system_instruction = "You are a helpful assistant. Use the following context and conversation history to answer."
            formatted_prompt = f"Context:\n{context}\n\nHistory:\n{history_str}\n\nQuestion: {user_prompt}"
            response = self.client.chat.completions.create(
                    model = Config.LLM_MODEL,
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
