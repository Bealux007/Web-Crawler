# Web-Crawler

**🚀 Renesas Web Crawler & Search Engine - README**


**📌 Project Overview**

The Renesas Web Crawler & Search Engine is an AI-powered system that:

Scrapes automotive design solutions from the Renesas website.
Indexes the extracted data using FAISS (Facebook AI Similarity Search).
Allows users to search for relevant designs using a Streamlit web interface.
This tool is built to crawl, extract, store, and search automotive engineering solutions using advanced NLP techniques and embedding-based search.

**🚀 Features**

✅ Automated Web Scraper – Extracts text and diagrams from Renesas pages.
✅ FAISS-Based Search Engine – Enables fast & efficient similarity search.
✅ Semantic Text Embeddings – Uses Sentence Transformers for improved text understanding.
✅ Streamlit UI – User-friendly web interface for searching relevant designs.
✅ PDF Export – Saves search results as PDF reports for offline reference.

**📂 Project Structure**

**📦 Renesas-Web-Crawler**

├── app.py                # Main Streamlit search application
├── Scraper.py            # Web scraper for extracting Renesas designs
├── indexing.py           # Builds FAISS index from extracted data
├── requirements.txt      # Python dependencies
├── renesas_data/         # Storage for scraped data
│   ├── designs.json      # JSON file storing extracted design descriptions
│   ├── design_index.bin  # FAISS index file for fast search
│   ├── design_embeddings.npy  # Stored embeddings of descriptions
│   ├── images/           # Extracted design SVG diagrams
└── README.md             # Documentation

**🛠 Technologies Used**

Streamlit 🎨	Provides an interactive UI for searching
FAISS 🚀	Enables fast similarity search for design retrieval
BeautifulSoup & Selenium 🌐	Web scraping for extracting text and SVG images
Sentence Transformers 🧠	Converts text into embeddings for search
Pillow 🖼️	Handles image processing
Requests 🔄	Fetches external data
ReportLab 📄	Generates PDF reports

**📜 File Descriptions**

**1️⃣ Scraper.py (Web Scraper)**

Extracts automotive design data from the Renesas website.
Uses Selenium & BeautifulSoup to:
Fetch titles, descriptions, and SVG diagrams from engineering pages.
Store extracted data in designs.json for later indexing.
Saves SVG diagrams separately in the images/ folder.

**2️⃣ indexing.py (Building the FAISS Index)**

Loads scraped design data from designs.json.
Converts text descriptions into semantic embeddings using Sentence Transformers.
Builds a FAISS index for fast retrieval.
Saves the processed embeddings and index for later use.

**3️⃣ app.py (Search Application)**
Provides a Streamlit-based UI for users to:
Enter search queries (e.g., "ADAS camera", "EV battery system").
Retrieve most relevant designs using FAISS similarity search.
View extracted SVG diagrams (if available).
Download search results as a PDF report.

**4️⃣ requirements.txt (Dependencies)**

Lists required Python libraries:

requests
beautifulsoup4
faiss-cpu
sentence-transformers
chromadb
streamlit
pillow
faiss-cpu: Enables fast search indexing.
sentence-transformers: Used for text embedding generation.
chromadb: Optional vector database integration.
pillow: Processes image files.

**🛠 Installation & Setup**

**1️⃣ Clone the Repository**

git clone https://github.com/Bealux007/Renesas-Web-Crawler.git
cd Renesas-Web-Crawler

**2️⃣ Create a Virtual Environment**

python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

**3️⃣ Install Dependencies**
pip install -r requirements.txt

**🚀 Running the Application**

**1️⃣ Run the Web Scraper**

**To extract Renesas designs:**

python Scraper.py
This fetches titles, descriptions, and diagrams from Renesas.
Saves data in renesas_data/designs.json.

**2️⃣ Build the FAISS Index**

Once the data is extracted:
python indexing.py
Converts text descriptions into embeddings.
Saves the FAISS index for later search queries.

**3️⃣ Launch the Search UI**

streamlit run app.py
Open the local Streamlit interface.
Enter search queries to find relevant Renesas designs.

**🔍 How It Works**

**1️⃣ Web Scraping Process**

Fetches titles, descriptions, and diagrams from Renesas application pages.
Stores the extracted data in designs.json.
Saves SVG diagrams in the images/ folder.

**2️⃣ Indexing & Search**

Converts design descriptions into embeddings.
Builds a FAISS-based similarity search index.
Allows fast search retrieval based on semantic meaning.

**3️⃣ Search & Retrieval UI**

Users enter keywords related to automotive designs.
The system finds top 3 relevant designs using FAISS similarity search.
Displays design descriptions & SVG diagrams.
Generates PDF reports of search results.

**🌟 Key Benefits**

✅ Automated Data Extraction – Scrapes real-time engineering solutions.
✅ AI-Powered Search Engine – Retrieves most relevant designs quickly.
✅ Scalable FAISS Indexing – Enables efficient search over large datasets.
✅ User-Friendly Interface – Provides an interactive search experience.
✅ PDF Export Functionality – Allows offline storage of results.

**🔮 Future Enhancements**

🔹 Real-Time Updates – Automate scraper to fetch new design updates daily.
🔹 Improve Image Processing – Enhance SVG diagram extraction.
🔹 Multi-Language Support – Add translation capabilities.
🔹 Deploy to Cloud – Host the search engine on a web server.

**📜 License**
This project is MIT Licensed.

**🔗 Contribute**
Pull requests are welcome! If you find a bug, open an issue.

