import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_vector_store(transcript_path, vector_dir="vector_db"):
    os.makedirs(vector_dir, exist_ok=True)

    with open(transcript_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_text(full_text)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(docs)

    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    base = os.path.splitext(os.path.basename(transcript_path))[0]
    faiss.write_index(index, os.path.join(vector_dir, f"{base}.index"))

    with open(os.path.join(vector_dir, f"{base}.pkl"), "wb") as f:
        pickle.dump(docs, f)

    print(f"✅ Vector store created for: {base}")
    return base