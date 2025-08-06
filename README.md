# AI Cover Letter Generator

A Python application that generates tailored cover letters based on a given CV and a list of job descriptions (URLs). Each letter is saved as a well-formatted .txt file in a destination folder of your choice.

This project is designed for local usage only, aimed at streamlining the application process by automating letter writing using LLMs such as Mistral or LLaMA via the Groq API.

## Features

- **CV Extraction**: Extracts full text content from a CV in PDF format
- **Job Scraping**: Scrapes job descriptions from provided URLs
- **AI Generation**: Generates a custom cover letter using your selected LLM
- **Organized Storage**: Saves each letter to a destination folder with formatting and clean filenames
- **Structured Output**: Outputs include a title and a formatted body for each cover letter

## Modern Web Interface

This application features a beautiful Streamlit web interface:

-  **Web-based** - Runs in your browser
-  **Smart preview** - See generated letters instantly
-  **Responsive design** - Works on any screen size
- 🌍 **Multilingual** - Auto-detects job language

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/cover-letter-generator.git
cd cover-letter-generator
```

### 2. Install Poetry (if not already installed)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. Install dependencies
```bash
poetry lock
poetry install
```

### 4. Set up environment variables
Create a `.env` file at the root of the `app/` directory with the following variables:

```env
# Path to your CV in PDF format
CV_PATH=/absolute/path/to/your/CV.pdf

# Folder where cover letters will be saved
DESTINATION_PATH=/absolute/path/to/output/folder

# Your preferred model (see model list below)
MODEL=mistral-saba-24b

# Your Groq API key
GROQ_API_KEY=your_api_key_here
```

## 🚀 Running the Application

```bash
poetry run streamlit run app/streamlit_app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### Alternative: Run with custom port
```bash
poetry run streamlit run app/streamlit_app.py --server.port 8080
```

## Supported LLM Models (Preview Only)

You must set the `MODEL` variable in your `.env` file to one of the following preview models from Groq:

| Model ID | Developer |
|----------|-----------|
| `deepseek-r1-distill-llama-70b` | DeepSeek |
| `meta-llama/llama-4-maverick-17b-128e-instruct` | Meta |
| `meta-llama/llama-4-scout-17b-16e-instruct` | Meta |
| `meta-llama/llama-prompt-guard-2-22m` | Meta |
| `meta-llama/llama-prompt-guard-2-86m` | Meta |
| `mistral-saba-24b` | Mistral AI |
| `moonshotai/kimi-k2-instruct` | Moonshot AI |
| `playai-tts` | PlayAI |
| `playai-tts-arabic` | PlayAI |
| `qwen/qwen3-32b` | Alibaba Cloud |

**Note**: These models are for preview only. They may be deprecated or removed without notice.

## How It Works

### CV Parsing
The `PdfManager` class extracts the full text from your CV.

### Job Description Retrieval
The `ApplicationManager` scrapes content from each job URL using a custom `Scraper`.

### Cover Letter Generation
The `Generator` class pipes the prompt and the CV + job description to the model, returning a structured `CoverLetterSchema`.

### File Output
The `CoverLetterManager` formats and writes the output letter to your destination directory as a `.txt` file.

## Example Usage

```python
# List of job URLs
urls = [
    "https://www.example.com/job/software-engineer",
    "https://www.example.com/job/data-scientist"
]

# Initialize generator
generator = Generator(urls)

# Run generation
results = generator.run()

# Display results
for letter in results:
    print(letter.title)
```

## Project Structure

```
app/
├── main.py                 # Main entry point
├── .env                    # Environment variables
├── utils/                  # Utility modules
│   ├── prompts.py         # Prompt templates
│   └── models.py          # Model definitions
├── tools/                  # Processing tools
│   ├── file_manager.py    # File management utilities
│   └── scraper.py         # Web scraping functionality
├── schema/                 # Data schemas
│   └── letter_schema.py   # Cover letter schema
└── ...
```

## Known Issues / Bugs to Fix

- **AI Detection**: Content is not sufficiently undetectable by AI detectors — to be improved by integrating a paid model
- **URL Handling**: Bug in URL handling causes infinite loop — needs correction to properly manage malformed or unexpected URLs
- **Letter Quality**: Quality of generated cover letters requires enhancement for better relevance and coherence
- **Style & Layout**: Improvement needed in the style and layout of cover letters to ensure professional and polished presentation
- **Multi Threading**: Add Multi Threading system to handle each generation seperatly

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.