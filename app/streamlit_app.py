"""
Modern Streamlit UI for AI Cover Letter Generator with Enhanced Features
"""

import streamlit as st
import os
import sys
import subprocess
import platform
from pathlib import Path
import pdfplumber
import warnings

# Add app directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator.generator import Generator
from config import get_api_key, AVAILABLE_MODELS, validate_api_key

# Suppress PDF warnings
warnings.filterwarnings('ignore', message='.*FontBBox.*')
warnings.filterwarnings('ignore', message='.*Could get FontBBox.*')

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

def extract_pdf_text(uploaded_file):
    """Extract text from uploaded PDF file."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with pdfplumber.open(uploaded_file) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text(x_tolerance=1.5, y_tolerance=2)
                    if page_text:
                        text += page_text + '\n'
                return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def main():
    # Initialize session state
    if 'cv_content' not in st.session_state:
        st.session_state.cv_content = None
    if 'cv_filename' not in st.session_state:
        st.session_state.cv_filename = None
    if 'destination_path' not in st.session_state:
        st.session_state.destination_path = str(Path.home() / "Documents" / "CoverLetters")
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = AVAILABLE_MODELS[0]
        
    # Check API key
    if not validate_api_key():
        st.error("⚠️ GROQ_API_KEY not found in environment variables. Please set it up before using the app.")
        st.info("Set GROQ_API_KEY in your .env file or environment variables.")
        st.stop()
    
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
        
        # CV Upload
        st.markdown("### 📄 CV Upload")
        uploaded_file = st.file_uploader(
            "Choose your CV (PDF)",
            type=['pdf'],
            key="cv_uploader",
            help="Upload your CV in PDF format"
        )
        
        if uploaded_file is not None:
            # Extract text from PDF
            cv_text = extract_pdf_text(uploaded_file)
            if cv_text:
                st.session_state.cv_content = cv_text
                st.session_state.cv_filename = uploaded_file.name
                st.success(f"✅ CV loaded: {uploaded_file.name}")
                with st.expander("Preview CV (first 500 chars)"):
                    st.text(cv_text[:500] + "..." if len(cv_text) > 500 else cv_text)
        elif st.session_state.cv_filename:
            st.info(f"Using: {st.session_state.cv_filename}")
        
        st.markdown("---")
        
        # Destination Folder
        st.markdown("### 📁 Output Folder")
        destination = st.text_input(
            "Destination path",
            value=st.session_state.destination_path,
            key="destination_input",
            help="Enter the full path where cover letters will be saved"
        )
        
        # Validate and create directory
        if destination:
            try:
                Path(destination).mkdir(parents=True, exist_ok=True)
                st.session_state.destination_path = destination
                if st.button("📂 Open Folder", key="open_dest"):
                    open_folder(destination)
            except Exception as e:
                st.error(f"Invalid path: {e}")
        
        st.markdown("---")
        
        # Model Selection
        st.markdown("### 🤖 Model Selection")
        selected_model = st.selectbox(
            "Choose AI Model",
            options=AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(st.session_state.selected_model),
            key="model_selector",
            help="Select the Groq model to use for generation"
        )
        st.session_state.selected_model = selected_model
        
        # Model descriptions
        model_info = {
            "llama-3.3-70b-versatile": "Best overall performance",
            "llama-3.1-8b-instant": "Fast and efficient",
            "gemma2-9b-it": "Good for instructions",
            "mixtral-8x7b-32768": "Large context window"
        }
        if selected_model in model_info:
            st.caption(model_info[selected_model])
        
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
        
        # Status Summary
        st.markdown("### 📊 Status")
        status_items = [
            ("CV", "✅" if st.session_state.cv_content else "❌"),
            ("Output", "✅" if st.session_state.destination_path else "❌"),
            ("Model", "✅"),
            ("API Key", "✅" if get_api_key() else "❌")
        ]
        for item, status in status_items:
            st.write(f"{item}: {status}")
    
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
            st.info("Language will be auto-detected from each job posting")
    
    # Generate button
    st.markdown("---")
    
    # Check if ready to generate
    can_generate = valid_urls and st.session_state.cv_content and st.session_state.destination_path
    
    if not st.session_state.cv_content:
        st.warning("⚠️ Please upload your CV in the sidebar before generating cover letters.")
    
    if st.button("Generate Cover Letters", type="primary", use_container_width=True, disabled=not can_generate):
        if not valid_urls:
            st.error("Please enter at least one URL")
            return
        
        if not st.session_state.cv_content:
            st.error("Please upload your CV first")
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
                # Initialize generator with user-provided parameters
                status_text.text("Initializing generator...")
                generator = Generator(
                    urls=valid_urls,
                    cv_content=st.session_state.cv_content,
                    destination_path=st.session_state.destination_path,
                    model_name=st.session_state.selected_model
                )
                
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
                            st.info(f"📁 Files saved to: {st.session_state.destination_path}")
                        with col2:
                            if st.button("📂 Open Folder", key="open_results"):
                                open_folder(st.session_state.destination_path)
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
            <p style="font-size: 0.9em;">Supports: 🇬🇧 English | 🇫🇷 Français | 🇳🇱 Nederlands | 🇩🇪 Deutsch | 🇪🇸 Español | 🇮🇹 Italiano</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()