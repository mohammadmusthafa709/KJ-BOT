from sentence_transformers import SentenceTransformer
import json
import faiss
import numpy as np

# Load the structured JSON data
with open("structured_data.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Load the embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Prepare data for FAISS
texts = [item["content"] for item in data]
urls = [item["url"] for item in data]

# Convert text to embeddings
embeddings = model.encode(texts, convert_to_numpy=True)

# Initialize FAISS index
embedding_dim = embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(embedding_dim)  # L2 similarity search
faiss_index.add(embeddings)

# Save FAISS index
faiss.write_index(faiss_index, "college_faiss.index")

# Save URLs mapping separately
with open("urls_mapping.json", "w", encoding="utf-8") as f:
    json.dump(urls, f, indent=4, ensure_ascii=False)

print("FAISS index and URL mapping saved successfully!")
