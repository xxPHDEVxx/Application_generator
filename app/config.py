"""
Simple configuration management for environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in app directory
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Configuration values
CV_PATH = os.getenv("CV_PATH", "")
DESTINATION_PATH = os.getenv("DESTINATION_PATH", "")
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Validate required configuration
if not CV_PATH or not Path(CV_PATH).exists():
    raise ValueError(f"CV_PATH not set or file doesn't exist: {CV_PATH}")

if not DESTINATION_PATH:
    raise ValueError("DESTINATION_PATH environment variable is not set")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

# Create destination directory if it doesn't exist
Path(DESTINATION_PATH).mkdir(parents=True, exist_ok=True)