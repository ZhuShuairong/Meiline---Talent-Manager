Digital Talent Assistant
This project is a web scraping and RAG (Retrieval-Augmented Generation) system designed to collect trending topics from various platforms and provide insights via a conversational interface. It scrapes data from platforms like 抖音 (Douyin), 哔哩哔哩 (Bilibili), IMDB, AcFun, and 知乎 (Zhihu), stores the data in a vector database, and uses a local LLM (Qwen3:4b via Ollama) to answer user queries about digital talent trends.
Project Structure

scrape.py: Scrapes trending data from specified platforms and saves it to a CSV file.
vector.py: Converts CSV data into LangChain Document objects and stores them in a Chroma vector database.
scheduler.py: Schedules the scraping process to run at :00 and :30 every hour.
main.py: Provides a Gradio-based chat interface for users to query trends using a RAG pipeline.

Flowchart
Below is a flowchart illustrating how the system operates:
graph TD
    A[Start] --> B[Scheduler runs every minute]
    B -->|At :00 or :30| C[Execute scrape.py]
    C --> D[Fetch webpages from platforms]
    D -->|Random headers| E[Scrape HTML content]
    E --> F[Extract nodes and entries]
    F --> G[Save data to output.csv]
    G --> H[vector.py loads CSV]
    H --> I[Convert to LangChain Documents]
    I --> J[Embed documents in ChromaDB]
    J --> K[Delete output.csv]
    J --> L[main.py initializes Gradio UI]
    L --> M[User submits query]
    M --> N[Retrieve relevant docs from ChromaDB]
    N --> O[Format prompt with RAG template]
    O --> P[Query Ollama LLM Qwen3:4b]
    P --> Q[Format response with Markdown]
    Q --> R[Display response in Gradio UI]

Requirements
See requirements.txt for the list of required Python packages.
Setup Instructions

Install Dependencies:
pip install -r requirements.txt


Install Ollama:

Follow instructions at Ollama's official site to install Ollama.
Pull the required models:ollama pull qwen3:4b
ollama pull nomic-embed-text:v1.5




Run the Scheduler:
python scheduler.py

This will run scrape.py at :00 and :30 every hour to collect data.

Run the Chat Interface:
python main.py

This launches the Gradio interface at http://localhost:7860 (or another port if specified).


Usage

Scheduler: Automatically runs the scraper twice per hour to keep the data fresh.
Chat Interface: Open the Gradio UI in your browser and ask questions like:
"What's popular on 抖音?"
"What are the latest hot topics?"
"What should I make a video about?"


The system retrieves relevant scraped data and uses the Qwen3:4b model to generate informed responses.

Notes

The scraper uses random user agents to avoid being blocked.
Data is stored in a Chroma vector database for efficient retrieval.
The CSV file (output.csv) is deleted after embedding to save space.
Ensure Ollama is running locally before starting the application.
