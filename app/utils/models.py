from langchain_groq import ChatGroq
from config import GROQ_API_KEY, MODEL

class Models:
    """
    Manages LLM model instances and configurations.
    """
    
    # Create the model instance
    MISTRAL = ChatGroq(
        model=MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.7,
        max_tokens=2000,
        timeout=60,
        max_retries=2
    )