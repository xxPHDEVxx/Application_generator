"""
Flexible configuration management for environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Try to load environment variables from .env file if it exists
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Configuration values with defaults
CV_PATH = os.getenv("CV_PATH", "")
DESTINATION_PATH = os.getenv("DESTINATION_PATH", str(Path.home() / "Documents" / "CoverLetters"))
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Available models for the UI
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it"
]

# Only validate GROQ_API_KEY as it's always required
# Other values can be provided through the UI
def validate_api_key():
    """Validate that GROQ_API_KEY is set."""
    if not GROQ_API_KEY:
        return False
    return True

# Create destination directory if path is set and valid
if DESTINATION_PATH:
    try:
        Path(DESTINATION_PATH).mkdir(parents=True, exist_ok=True)
    except Exception:
        pass  # Directory creation might fail, handle in UI