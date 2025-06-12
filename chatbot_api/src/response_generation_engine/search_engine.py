# File: search_engine.py
from sentence_transformers import SentenceTransformer
from response_generation_engine.docx_preprocessing import DataExtraction
import os 
import numpy as np 
import pickle 
import dotenv 
import faiss

dotenv.load_dotenv()

class VectorSearchEngine: 
    def __init__(self, data_directory, model_name="all-MiniLM-L6-v2"):
        self.data_directory = data_directory
        print("Loading the docx files and text splitting")
        load_and_chunk = DataExtraction(self.data_directory)
        self.all_Chunks = load_and_chunk.docx_chunk_pipeline()

        print("Loading embedding model")
        self.model_name = model_name 
        self.embedder = SentenceTransformer(self.model_name)

        self.output_path = os.path.join(os.path.dirname(self.data_directory), "Output")
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        self.index_path = os.path.join(self.output_path, "faiss_index.index")
        self.metadata_path = os.path.join(self.output_path, "metadata.pkl")
    
    def encode_text(self, texts): 
        """
        Encoding the texts (this can be a single text or batch of texts).
        """
        return self.embedder.encode(texts, show_progress_bar=True) 
     
    def build_search_index(self):
        """
        Build a search index from JSON files.
        """
        all_texts = [chunk['content'] for chunk in self.all_Chunks]
        
        # Encode all texts
        embeddings = self.embedder.encode(all_texts, show_progress_bar=True)
        # Create a FAISS index
        embeddings_matrix = np.array(embeddings).astype(np.float32)
        vector_index = faiss.IndexFlatL2(embeddings_matrix.shape[1])
        vector_index.add(embeddings_matrix)

        self.vector_index = vector_index 
        self.metadata_store = all_texts
        
        self.save(index_path=self.index_path, metadata_path=self.metadata_path)
        print(f"Index saved to {self.index_path} and metadata saved to {self.metadata_path}")

        return self.vector_index, self.metadata_store

    def save(self, index_path, metadata_path):
        faiss.write_index(self.vector_index, index_path)
        import pickle
        with open(metadata_path, "wb") as f:
            pickle.dump(self.metadata_store, f)

    def load_vector_index(self, index_path="faiss_index.index", metadata_path="metadata.pkl"):
        self.vector_index = faiss.read_index(index_path)
        with open(metadata_path, "rb") as f:
            self.metadata_store = pickle.load(f)
        return self.vector_index, self.metadata_store

    def vector_similarity_search(self, query, k=5):
        """
        Perform a vector similarity search.
        """
        query_embedding = self.embedder.encode([query]).astype(np.float32)
        distances, indices = self.vector_index.search(query_embedding, k)
        results = [self.metadata_store[idx] for idx in indices[0]]
        return "\n\n".join(results)

if __name__ == "__main__":
    search_engine = VectorSearchEngine(data_directory=r"C:\Users\LENOVO\Desktop\Projects\RAG_based_app_sector_expert\Data")
    vector_index, metadata_store = search_engine.build_search_index()
    print("Vector index and metadata store built successfully.")
    answer = search_engine.vector_similarity_search("What is Vietnam's position in the world's evolving geopolitical landscape", k=5)
    print("Search Results: ", answer)