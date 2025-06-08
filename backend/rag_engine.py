import faiss
import pickle
import os
from transformers import AutoTokenizer, AutoModelForCausalLM

class RAGEngine:
    def __init__(self, vector_db_path: str, model_name="microsoft/phi-2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.vector_db_path = vector_db_path

    def load_vector_store(self, base_name: str):
        index_path = os.path.join(self.vector_db_path, f"{base_name}.index")
        text_path = os.path.join(self.vector_db_path, f"{base_name}.pkl")

        self.index = faiss.read_index(index_path)
        with open(text_path, "rb") as f:
            self.docs = pickle.load(f)

    def retrieve_context(self, query: str, top_k=3):
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        query_vec = model.encode([query])
        D, I = self.index.search(query_vec, top_k)
        return [self.docs[i] for i in I[0]]

    def generate_answer(self, query: str, base_name: str):
        self.load_vector_store(base_name)
        context = self.retrieve_context(query)

        prompt = f"""
You are a helpful assistant. Based on the following transcript context, answer the user's question.

Transcript:
{chr(10).join(context)}

Question:
{query}

Answer:
"""

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
        output = self.model.generate(**inputs, max_length=512)
        answer = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return answer.split("Answer:")[-1].strip()