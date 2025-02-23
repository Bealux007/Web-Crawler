import os
import json
import faiss
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Paths
SAVE_DIR = "renesas_data"
JSON_PATH = os.path.join(SAVE_DIR, "designs.json")
INDEX_PATH = os.path.join(SAVE_DIR, "design_index.bin")
EMBEDDINGS_PATH = os.path.join(SAVE_DIR, "design_embeddings.npy")
IMAGE_DIR = os.path.join(SAVE_DIR, "images")
PDF_PATH = os.path.join(SAVE_DIR, "search_results.pdf")

# Load Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load Designs
if os.path.exists(JSON_PATH):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        designs = json.load(f)
else:
    st.error("❌ No designs found! Run `scraper.py` first.")
    designs = []

# Load FAISS Index
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    st.error("⚠️ FAISS index not found! Run `indexing.py` first.")
    index = None


def search_designs(query, top_k=3):
    """Searches for the top K relevant designs."""
    if not index or len(designs) == 0:
        return []

    query_embedding = model.encode([query], normalize_embeddings=True)
    distances, indices = index.search(np.array(query_embedding, dtype=np.float32), top_k)

    results = []
    for i in range(len(indices[0])):
        idx = indices[0][i]
        if 0 <= idx < len(designs):  # Avoid IndexError
            results.append(designs[idx])

    return results


def save_query_to_pdf(query, results):
    """Saves search query and results to a PDF file."""
    c = canvas.Canvas(PDF_PATH, pagesize=letter)
    c.setFont("Helvetica", 12)

    y = 750
    c.drawString(50, y, f"Search Query: {query}")
    y -= 20

    for result in results:
        title = result.get("title", "No Title")
        description = result.get("description", "No Description")
        svg_path = result.get("svg_path", "No Image Available")

        c.drawString(50, y, f"Title: {title}")
        y -= 20
        c.drawString(50, y, f"Description: {description[:150]}...")  # Truncate long descriptions
        y -= 20
        c.drawString(50, y, f"SVG Path: {svg_path}")
        y -= 40  # Space between results

        if y < 100:  # Avoid writing past the page bottom
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750

    c.save()


# Streamlit UI
st.title("🔍 Renesas ADAS Design Search")
query = st.text_input("Enter a keyword (e.g., 'ADAS camera', 'autonomous driving'): ")

if query:
    results = search_designs(query)

    if results:
        st.write(f"### Results for: {query}")
        
        for design in results:
            st.subheader(design["title"])
            st.write(design["description"])

            # Display SVG Image
            svg_path = design.get("svg_path", "")
            if svg_path and os.path.exists(svg_path):
                st.image(svg_path, caption="Design Diagram", use_container_width=True)
            else:
                st.warning("⚠️ SVG Image not found.")

        # Save the query and results to a PDF
        save_query_to_pdf(query, results)
        st.success("✅ Query and results saved to PDF!")

        # Provide a download button
        with open(PDF_PATH, "rb") as pdf_file:
            st.download_button("📥 Download Search Results (PDF)", pdf_file, file_name="search_results.pdf")

    else:
        st.error("🚫 No matching designs found.")
