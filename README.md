📝 AI Cover Letter Generator

This Python application generates tailored cover letters based on a given CV and a list of job descriptions (URLs). Each letter is saved as a well-formatted .txt file in a destination folder of your choice.

This project is for local usage only, designed to streamline the application process by automating letter writing using LLMs such as Mistral or LLaMA via the Groq API.

Features

📄 Extracts full text content from a CV (PDF format)
🌐 Scrapes job descriptions from provided URLs
🤖 Generates a custom cover letter using your selected LLM
📁 Saves each letter to a destination folder with formatting and clean filenames
💬 Outputs include a title and a formatted body for each cover letter
🔧 Installation & Setup

Clone the repository
git clone https://github.com/your-username/cover-letter-generator.git
cd cover-letter-generator

🔧 Installation & Setup

Clone the repository
git clone https://github.com/your-username/cover-letter-generator.git
cd cover-letter-generator
Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -
Install dependencies
poetry lock
poetry install
Set up environment variables
Create a .env file at the root of the app/ directory with the following variables:

# Path to your CV in PDF format
CV_PATH=/absolute/path/to/your/CV.pdf

# Folder where cover letters will be saved
DESTINATION_PATH=/absolute/path/to/output/folder

# Your preferred model (see model list below)
MODEL=mistral-saba-24b

# Your Groq API key
GROQ_API_KEY=your_api_key_here


🤖 Supported LLM Models (Preview Only)

You must set the MODEL variable in your .env file to one of the following preview models from Groq:

MODEL ID	DEVELOPER
deepseek-r1-distill-llama-70b	DeepSeek
meta-llama/llama-4-maverick-17b-128e-instruct	Meta
meta-llama/llama-4-scout-17b-16e-instruct	Meta
meta-llama/llama-prompt-guard-2-22m	Meta
meta-llama/llama-prompt-guard-2-86m	Meta
mistral-saba-24b	Mistral AI
moonshotai/kimi-k2-instruct	Moonshot AI
playai-tts	PlayAI
playai-tts-arabic	PlayAI
qwen/qwen3-32b	Alibaba Cloud
Note: These models are for preview only. They may be deprecated or removed without notice.


How It Works

CV Parsing
The PdfManager class extracts the full text from your CV.
Job Description Retrieval
The ApplicationManager scrapes content from each job URL using a custom Scraper.
Cover Letter Generation
The Generator class pipes the prompt and the CV + job description to the model, returning a structured CoverLetterSchema.
File Output
The CoverLetterManager formats and writes the output letter to your destination directory as a .txt file.

Example Usage

You can call the generator with a list of URLs like so:

urls = [
    "https://www.example.com/job/software-engineer",
    "https://www.example.com/job/data-scientist"
]

generator = Generator(urls)
results = generator.run()

for letter in results:
    print(letter.title)

Project Structure

app/
├── main.py
├── .env
├── utils/
│   ├── prompts.py
│   └── models.py
├── tools/
│   ├── file_manager.py
│   └── scraper.py
├── schema/
│   └── letter_schema.py
└── ...


Bugs to Fix / known issues

-   Content is not sufficiently undetectable by AI detectors — to be improved by integrating a paid model.
-   Bug in URL handling causes infinite loop — needs correction to properly manage malformed or unexpected URLs.
-   Quality of generated cover letters requires enhancement for better relevance and coherence.
-   Improvement needed in the style and layout of cover letters to ensure professional and polished presentation.