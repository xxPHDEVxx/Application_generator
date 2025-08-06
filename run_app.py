#!/usr/bin/env python3
"""
Launch script for AI Cover Letter Generator
Allows user to choose between Tkinter and Streamlit UI
"""

import sys
import os
import subprocess

def run_tkinter():
    """Run the Tkinter UI"""
    print("Starting Tkinter UI...")
    sys.path.append('app')
    from main import CoverLetterGeneratorUI
    import tkinter as tk
    
    root = tk.Tk()
    app = CoverLetterGeneratorUI(root)
    root.mainloop()

def run_streamlit():
    """Run the Streamlit UI"""
    print("🚀 Starting Streamlit UI...")
    print("📍 The app will open in your browser automatically\n")
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "app/streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "localhost"
    ])

def main():
    print("=" * 60)
    print("       AI COVER LETTER GENERATOR")
    print("=" * 60)
    print("\nChoose your interface:\n")
    print("1. 🖥️  Tkinter (Classic Desktop UI)")
    print("2. 🌐 Streamlit (Modern Web UI) - RECOMMENDED")
    print("3. ❌ Exit")
    print()
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            run_tkinter()
            break
        elif choice == "2":
            run_streamlit()
            break
        elif choice == "3":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()