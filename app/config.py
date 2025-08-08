"""
Flexible configuration management for environment variables.
Supports both local .env files and Streamlit secrets.
"""

import os
from pathlib import Path

# Try to import streamlit for secrets
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

# Try to load dotenv for local development
try:
    from dotenv import load_dotenv
    # Load .env file if it exists
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass  # dotenv not available, likely in deployment

def get_api_key():
    """Get API key from environment or Streamlit secrets."""
    # Try Streamlit secrets first (for deployment)
    if HAS_STREAMLIT:
        try:
            # Check if we're in a Streamlit app context
            if hasattr(st, 'secrets') and "GROQ_API_KEY" in st.secrets:
                return st.secrets["GROQ_API_KEY"]
        except Exception:
            pass
    
    # Fall back to environment variable
    return os.getenv("GROQ_API_KEY", "")

# Configuration values with defaults
CV_PATH = os.getenv("CV_PATH", "")
DESTINATION_PATH = os.getenv("DESTINATION_PATH", str(Path.home() / "Documents" / "CoverLetters"))
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")
GROQ_API_KEY = get_api_key()

# Available models for the UI
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it"
]

# Only validate GROQ_API_KEY as it's always required
def validate_api_key():
    """Validate that GROQ_API_KEY is set."""
    api_key = get_api_key()
    return bool(api_key and len(api_key) > 10)

# Create destination directory if path is set and valid
if DESTINATION_PATH:
    try:
        Path(DESTINATION_PATH).mkdir(parents=True, exist_ok=True)
    except Exception:
        pass  # Directory creation might fail, handle in UI