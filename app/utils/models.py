from langchain_groq import ChatGroq
from config import get_api_key, MODEL

class Models:
    """
    Manages LLM model instances and configurations.
    """
    
    _instances = {}
    
    @classmethod
    def get_model(cls, model_name=None):
        """Get or create a model instance for the specified model"""
        # Use provided model name or fall back to config
        model_to_use = model_name or MODEL
        
        # Check if we already have an instance for this model
        if model_to_use not in cls._instances:
            api_key = get_api_key()
            if not api_key:
                raise ValueError("GROQ_API_KEY not set. Please set it in .env file or Streamlit secrets.")
            
            cls._instances[model_to_use] = ChatGroq(
                model=model_to_use,
                api_key=api_key,
                temperature=0.7,
                max_tokens=2000,
                timeout=60,
                max_retries=2
            )
        return cls._instances[model_to_use]
    
    # Create a class-level attribute for backward compatibility
    MISTRAL = None
    
    def __class_getattr__(cls, name):
        """Handle dynamic attribute access for backward compatibility"""
        if name == "MISTRAL":
            return cls.get_model()
        raise AttributeError(f"'{cls.__name__}' object has no attribute '{name}'")