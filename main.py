from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import get_retriever
import gradio as gr
import re

# Initialize local Ollama LLM with Qwen3:4b model
llm = OllamaLLM(model="qwen3:4b",
                temperature=0.6,
                TopP=0.95,
                TopK=20,
                minP=0)

# Define the RAG prompt template
RAG_PROMPT_TEMPLATE = """You are a helpful digital talent manager. Use the following context to answer the user's question:

Context in the format of (ranking, source, title, datetime): {context}

Question: {question}

Answer:"""

def format_response(response):
    """Format the response with Markdown styling and collapsible sections"""
    # Convert **text** to bold Markdown
    response = re.sub(r'\*\*(.*?)\*\*', r'**\1**', response)
    
    # Handle <think> sections (make them collapsible)
    response = re.sub(
        r'<think>(.*?)</think>', 
        r'<details><summary>Thinking Process (Click to expand)</summary>\n\n\1\n\n</details>', 
        response, 
        flags=re.DOTALL
    )
    return response

def rag_chain(query, history=None):
    """Process the user query and return a formatted response"""
    # Get relevant documents from vector store
    retriever = get_retriever()
    relevant_docs = retriever.invoke(query)
    
    # Format context from retrieved documents
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # Create prompt with context and query
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    formatted_prompt = prompt.format(context=context, question=query)
    
    # Get response from local LLM
    response = llm.invoke(formatted_prompt)
    return format_response(response)

# Create Gradio ChatInterface for a Grok-like conversational UI
def create_chat_interface():
    return gr.ChatInterface(
        fn=rag_chain,
        chatbot=gr.Chatbot(
            label="Meiline",
            height=650,
            type="messages",  # Explicitly set to modern openai-style format
            avatar_images=(None, "https://tse3.mm.bing.net/th/id/OIP.U_uIr_PnVMLqWKqbKqTe8gAAAA?w=400&h=400&rs=1&pid=ImgDetMain&o=7&rm=3"),  # Placeholder for assistant avatar
        ),
        textbox=gr.Textbox(
            placeholder="Ask about digital talent trends or platforms like 抖音, 哔哩哔哩, or IMDB...",
            label="Type your question"
        ),
        title="Meiline - Your Digital Talent Assistant",
        description="I'm here to help you navigate the latest trends in digital entertainment! Ask about hot topics, video ideas, or what's trending on platforms like 抖音, 哔哩哔哩, or IMDB.",
        examples=[
            ["What are the latest hot topics?"],
            ["What should I make a video about?"],
            ["What's popular right now on 抖音?"],
            ["What's popular right now on 哔哩哔哩?"],
            ["What are some popular movies on IMDB?"],
            ["What's the latest news on 知乎?"],
            ["What's the latest news on acfun?"],
        ],
        theme=gr.themes.Soft(),  # Clean, modern theme similar to Grok's aesthetic
        css="""
            .chatbot .message { border-radius: 10px; padding: 10px; }
            .user-message { background-color: #f0f0f0; }
            .bot-message { background-color: #e6f3ff; }
            .gr-button { border-radius: 8px; }
            .gr-textbox { border-radius: 8px; }
        """
    )

if __name__ == "__main__":
    chat_interface = create_chat_interface()
    chat_interface.launch()