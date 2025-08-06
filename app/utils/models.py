from langchain_groq import ChatGroq
from config import GROQ_API_KEY, MODEL

class Models:
    """
    Manages LLM model instances and configurations.
    """
    
    _instance = None
    
    @classmethod
    def get_model(cls):
        """Get or create the model instance (lazy initialization)"""
        if cls._instance is None:
            if not GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not set in environment variables")
            
            cls._instance = ChatGroq(
                model=MODEL,
                api_key=GROQ_API_KEY,
                temperature=0.7,
                max_tokens=2000,
                timeout=60,
                max_retries=2
            )
        return cls._instance
    
    # Create a class-level attribute for backward compatibility
    MISTRAL = None
    
    def __class_getattr__(cls, name):
        """Handle dynamic attribute access for backward compatibility"""
        if name == "MISTRAL":
            return cls.get_model()
        raise AttributeError(f"'{cls.__name__}' object has no attribute '{name}'")