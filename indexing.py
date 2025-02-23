import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
SAVE_DIR = "renesas_data"
JSON_PATH = os.path.join(SAVE_DIR, "designs.json")
INDEX_PATH = os.path.join(SAVE_DIR, "design_index.bin")
EMBEDDINGS_PATH = os.path.join(SAVE_DIR, "design_embeddings.npy")

# Load Sentence Transformer for text embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

def build_index():
    """Creates a FAISS index from design JSON data for all scraped URLs."""
    
    if not os.path.exists(JSON_PATH):
        print("❌ JSON file not found! Run `scraper.py` first.")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        designs = json.load(f)

    if not designs:
        print("⚠️ No designs found in JSON! Check if `scraper.py` fetched any data.")
        return

    # Extract titles & descriptions for embeddings
    texts = []
    valid_designs = []  # Keep track of valid entries to maintain index order

    for design in designs:
        if "title" in design and "description" in design:
            text = f"{design['title']} {design['description']}"
            texts.append(text)
            valid_designs.append(design)  # Maintain a valid mapping
        else:
            print(f"⚠️ Skipping entry due to missing fields: {design}")

    if not texts:
        print("❌ No valid text data found for embeddings! Aborting indexing.")
        return

    # Generate embeddings for valid data
    embeddings = model.encode(texts, normalize_embeddings=True)
    np.save(EMBEDDINGS_PATH, embeddings)

    # Create FAISS index
    d = embeddings.shape[1]  # Vector dimension
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings, dtype=np.float32))

    # Save FAISS index
    faiss.write_index(index, INDEX_PATH)

    # Save only valid designs back to JSON (to maintain order in searches)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(valid_designs, f, indent=4)

    print(f"✅ FAISS Index successfully saved at {INDEX_PATH}")

def load_index():
    """Loads the FAISS index or builds it if missing."""
    if not os.path.exists(INDEX_PATH):
        print("⚠️ FAISS index not found! Building it now...")
        build_index()
    
    return faiss.read_index(INDEX_PATH)

if __name__ == "__main__":
    build_index()
