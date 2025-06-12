
import dotenv
import os 
from response_generation_engine.search_engine import VectorSearchEngine
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from chains.sector_investment_chains import review_template


dotenv.load_dotenv()

LLM_MODEL_NAME  = os.getenv("LLM_MODEL_NAME")
DATA_DIRECTORY = os.getenv("DATA_DIRECTORY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")


class Chatbot:
    def __init__(self, temperature=0.7, model_name=LLM_MODEL_NAME):
        self.model_name = model_name
        self.search_engine = VectorSearchEngine(DATA_DIRECTORY)
        self.embedder = self.search_engine.embedder
        self.index_path = self.search_engine.index_path
        self.metadata_path = self.search_engine.metadata_path
        # Load the FAISS Index and Metata 
        if not os.path.exists(self.index_path) or not os.path.exists(self.metadata_path):
            self.faiss_index, self.metadata_store = self.search_engine.build_search_index()
            print("Index and metadata created successfully.")
        else:
            self.faiss_index, self.metadata_store = self.search_engine.load_vector_index(self.index_path, self.metadata_path)
        # Initialize the chat model

        os.environ["OPENAI_API_KEY"] = OPENROUTER_API_KEY
        self.chat_pipeline = ChatOpenAI(
            base_url=LLM_BASE_URL,
            model_name=self.model_name,
            temperature=temperature
        )

     
    def query(self, question):
        """
        This function will be use to generate the response under hood of LLM including:
        1. Fetching top 5 the highest similarity score document as the context for LLM 
        2. Generate the response for the user's query using the LLM
        """
        # Perform Vector Similarity Search 
        context = self.search_engine.vector_similarity_search(query=question, k=5)
        prompt = review_template.format(
            context=context,
            question=question
        )
        # Generate the response using the chat model
        response = self.chat_pipeline([HumanMessage(content=prompt)])
        return response.content.strip()
     
if __name__ == "__main__":
    chatbot = Chatbot()
    
    question = "How stable of VND-USD exchange rate in 2022-2023"
    answer = chatbot.query(question)
    print("Answer:", answer)

    