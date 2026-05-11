import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Load the target document
# Change this filename to whatever PDF you have in the folder
PDF_PATH = "TitanVision_Interview_Guide_v1.pdf" 
print(f"Loading {PDF_PATH}...")
loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

# 2. The Chunker
# We split text so the AI can find specific "facts" rather than reading the whole file
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)python
chunks = text_splitter.split_documents(docs)
print(f"Split document into {len(chunks)} searchable chunks.")

# 3. The Embedding Engine (Optimized for Ryzen 5)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. The Vector Database (ChromaDB)
# This creates a folder named 'db' to store the vectors permanently
print("Vectorizing text and saving to local database...")
vector_db = Chroma.from_documents(
    documents=chunks, 
    embedding=embeddings, 
    persist_directory="./db"
)
print("Archimedes now remembers your document!")