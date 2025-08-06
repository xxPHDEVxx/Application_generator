"""
Modern Streamlit UI for AI Cover Letter Generator
"""

import streamlit as st
import os
import sys
import subprocess
import platform
from pathlib import Path
import time

# Add app directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator.generator import Generator
from config import CV_PATH, DESTINATION_PATH, MODEL

# Page configuration
st.set_page_config(
    page_title="AI Cover Letter Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: 500;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    div[data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

def open_folder(path):
    """Open folder in system file explorer"""
    try:
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", path])
        elif platform.system() == "Windows":
            subprocess.run(["explorer", path])
        else:  # Linux
            subprocess.run(["xdg-open", path])
        return True
    except Exception as e:
        st.error(f"Could not open folder: {e}")
        return False

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI Cover Letter Generator</h1>
        <p style="font-size: 1.2em; margin-top: 10px;">Generate professional cover letters in multiple languages</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Display current settings
        st.markdown("### Current Settings")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write("📄")
            st.write("📁")
            st.write("🤖")
        with col2:
            st.write("**CV:**")
            st.write("**Output:**")
            st.write("**Model:**")
        
        st.code(f"CV: {Path(CV_PATH).name if CV_PATH else 'Not set'}", language=None)
        st.code(f"Output: {Path(DESTINATION_PATH).name if DESTINATION_PATH else 'Not set'}", language=None)
        st.code(f"Model: {MODEL}", language=None)
        
        st.markdown("---")
        
        # Features list
        st.markdown("### ✨ Features")
        features = [
            "Automatic language detection",
            "Professional PDF generation",
            "Token optimization",
            "Multiple job applications",
            "Parallel processing"
        ]
        for feature in features:
            st.markdown(f"• {feature}")
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### 🎯 Quick Actions")
        if st.button("📂 Open Output Folder", use_container_width=True):
            if DESTINATION_PATH and Path(DESTINATION_PATH).exists():
                if open_folder(DESTINATION_PATH):
                    st.success("Folder opened!")
            else:
                st.error("Output folder not found")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Job Posting URLs")
        st.markdown("Enter the URLs of job postings you want to apply to:")
        
        # Initialize session state for URLs
        if 'urls' not in st.session_state:
            st.session_state.urls = ['']
        
        # URL input fields
        urls_to_remove = []
        for i, url in enumerate(st.session_state.urls):
            col_url, col_btn = st.columns([5, 1])
            with col_url:
                new_url = st.text_input(
                    f"URL {i+1}",
                    value=url,
                    key=f"url_{i}",
                    placeholder="https://example.com/job-posting",
                    label_visibility="collapsed"
                )
                st.session_state.urls[i] = new_url
            with col_btn:
                if st.button("🗑️", key=f"remove_{i}", help="Remove this URL"):
                    urls_to_remove.append(i)
        
        # Remove URLs marked for deletion
        for i in reversed(urls_to_remove):
            st.session_state.urls.pop(i)
        
        # Add URL button
        col_add, col_clear = st.columns(2)
        with col_add:
            if st.button("➕ Add Another URL", type="secondary", use_container_width=True):
                st.session_state.urls.append('')
                st.rerun()
        
        with col_clear:
            if st.button("🗑️ Clear All", type="secondary", use_container_width=True):
                st.session_state.urls = ['']
                st.rerun()
    
    with col2:        
        # Display stats
        valid_urls = [url for url in st.session_state.urls if url.strip()]
        
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("Total URLs", len(valid_urls))
        with metric_col2:
            st.metric("Ready", "✅" if valid_urls else "❌")
        
        # Language detection preview
        if valid_urls:
            st.markdown("### 🌍 Expected Languages")
            languages = ["🇬🇧 English", "🇫🇷 French", "🇳🇱 Dutch", "🇩🇪 German", "🇪🇸 Spanish", "🇮🇹 Italian"]
            st.info("Language will be auto-detected from each job posting")
    
    # Generate button
    st.markdown("---")
    
    if st.button("Generate Cover Letters", type="primary", use_container_width=True, disabled=not valid_urls):
        if not valid_urls:
            st.error("Please enter at least one URL")
            return
        
        # Create progress container
        progress_container = st.container()
        
        with progress_container:
            st.markdown("### Generation Progress")
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Results container
            results_container = st.container()
            
            try:
                # Initialize generator
                status_text.text("Initializing generator...")
                generator = Generator(valid_urls)
                
                # Simulate progress (in real app, update based on actual progress)
                status_text.text("Fetching job descriptions...")
                progress_bar.progress(25)
                
                status_text.text("Detecting languages...")
                progress_bar.progress(50)
                
                status_text.text("Generating cover letters...")
                progress_bar.progress(75)
                
                # Run generation
                results = generator.run()
                
                progress_bar.progress(100)
                status_text.text("✅ Generation complete!")
                
                # Display results
                if results:
                    with results_container:
                        st.success(f"🎉 Successfully generated {len(results)} cover letter(s)!")
                        
                        # Show generated letters
                        st.markdown("### 📄 Generated Cover Letters")
                        for i, letter in enumerate(results, 1):
                            with st.expander(f"📝 {letter.title}", expanded=(i==1)):
                                st.markdown(f"**Preview:**")
                                st.text(letter.content[:500] + "..." if len(letter.content) > 500 else letter.content)
                        
                        # Success message with folder button
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.info(f"📁 Files saved to: {DESTINATION_PATH}")
                        with col2:
                            if st.button("📂 Open Folder", key="open_results"):
                                open_folder(DESTINATION_PATH)
                else:
                    st.warning("No cover letters were generated. Please check the URLs.")
                    
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.exception(e)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; padding: 20px;">
            <p>Built using Streamlit | Powered by AI</p>
            <p style="font-size: 0.9em;">Supports: 🇬🇧 English | 🇫🇷 Français | 🇳🇱 Nederlands | 🇪🇸 Españo</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()