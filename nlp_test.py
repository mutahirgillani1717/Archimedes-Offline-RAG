from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize a lightweight, high-performance embedding model
# This runs perfectly on a Ryzen 5 CPU
print("Initializing Embedding Engine...")
embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

text = "AlphaForecast uses a Hybrid LSTM-GRU architecture."
vector = embed_model.embed_query(text)

print(f"Successfully converted text into a vector of length: {len(vector)}")
print("First 5 dimensions of the vector:", vector[:5])