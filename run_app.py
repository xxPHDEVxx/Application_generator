#!/usr/bin/env python3
"""
Launch script for AI Cover Letter Generator
"""

import sys
import subprocess

def main():
    print("=" * 60)
    print("       AI COVER LETTER GENERATOR")
    print("=" * 60)
    print("\n🚀 Starting Streamlit UI...")
    print("📍 The app will open in your browser automatically\n")
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "app/streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "localhost"
    ])

if __name__ == "__main__":
    main()