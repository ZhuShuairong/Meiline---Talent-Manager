import os
import csv
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_ollama import OllamaEmbeddings

# Configuration
PERSIST_DIRECTORY = "./chroma_db"
CSV_FILE = "output.csv"

# Define the embedding model using Ollama
embedding_model = OllamaEmbeddings(model="nomic-embed-text:v1.5")

def get_retriever():
    """Initialize and return a retriever from ChromaDB vector store."""
    print(f"Initializing ChromaDB from directory: {PERSIST_DIRECTORY}")
    
    if not os.path.exists(PERSIST_DIRECTORY):
        print("No existing ChromaDB found, creating new one...")
        # Load and prepare documents from CSV
        documents = load_documents_from_csv(CSV_FILE)
        print(f"Loaded {len(documents)} documents from CSV")
        
        if not documents:
            print("Warning: No documents loaded from CSV, check output.csv")
            return None
            
        print("Creating vector store...")
        vectorstore = Chroma.from_documents(
            documents, 
            embedding_model, 
            persist_directory=PERSIST_DIRECTORY
        )
        print("Vector store created successfully")
        
        # Delete the CSV file only after successful embedding
        if os.path.exists(CSV_FILE):
            print(f"Deleting CSV file: {CSV_FILE}")
            os.remove(CSV_FILE)
    else:
        print("Loading existing ChromaDB...")
        vectorstore = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding_model)
    
    # Create retriever with top 5 results
    retriever = vectorstore.as_retriever(search_kwargs={"k": 100})
    print("Retriever initialized successfully")
    return retriever

def load_documents_from_csv(csv_file):
    """Load and convert CSV data into LangChain Document objects."""
    print(f"Loading documents from CSV: {csv_file}")
    documents = []
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at {csv_file}")
        return documents
        
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, 1):
            # Combine title, node_name, and scrape_time into text content
            text = f"{row['rank']} {row['title']} {row['node_name']} {row['scrape_time']}"
            # Store link, extra and other fields as metadata
            metadata = {
                "node_id": row["node_id"],
                "link": row["link"],
                "extra": row["extra"]
            }
            documents.append(Document(page_content=text, metadata=metadata))
            if i % 10 == 0:
                print(f"Processed {i} rows...")
    
    print(f"Total documents loaded: {len(documents)}")
    return documents

if __name__ == "__main__":
    get_retriever()