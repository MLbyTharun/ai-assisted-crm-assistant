from langchain_groq import ChatGroq

def get_groq_llm(api_key: str):
    """
    Initializes and returns a Groq LLM instance using Llama 3.1.
    """
    if not api_key:
        raise ValueError("Groq API Key is required. Please provide it in the sidebar.")
        
    return ChatGroq(
        model="llama-3.1-8b-instant", 
        groq_api_key=api_key, 
        temperature=0.7
    )