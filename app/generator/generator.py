from utils.prompts import Prompt
from utils.models import Models
from utils.text_processor import TextProcessor
from utils.language_detector import LanguageDetector
from tools.file_manager import *
from schema.letter_schema import CoverLetterSchema

class Generator:
    """
    Class responsible for generating personalized cover letters 
    based on a given CV and a list of job descriptions.
    
    It uses a language model with structured output to produce 
    tailored letters and delegates saving to a file manager.
    """

    def __init__(self, urls: list[str]):
        """
        Initializes the Generator with a list of job posting URLs.

        Args:
            urls (list[str]): List of job offer URLs to process.
        """
        # Language model configured to return structured output following CoverLetterSchema
        self.model = Models.MISTRAL.with_structured_output(CoverLetterSchema)

        # Prompt template guiding the letter generation
        self.prompt = Prompt.GENERATE_MOTIVATION

        # Extract CV content automatically from a PDF
        self.cv = PdfManager().run()

        # Store the list of URLs to process
        self.urls = urls

    def run(self):
        """
        Executes the letter generation process for each job offer.

        Returns:
            list[CoverLetterSchema]: A list of generated cover letters 
            as structured data (title and content).
        """
        # Compose the prompt and model into a LangChain chain
        chain = self.prompt | self.model

        # Managers for saving letters and parsing job applications
        letter_manager = CoverLetterManager()
        application_manager = ApplicationManager(self.urls)

        # Retrieve job descriptions from the provided URLs
        applications = application_manager.run()

        # Store the resulting cover letters
        results = []

        for i, application in enumerate(applications):
            try:
                # Detect the language of the job posting
                language, confidence = LanguageDetector.detect_language(application)
                language_name = LanguageDetector.get_language_name(language)
                
                print(f"📌 Job {i+1}/{len(applications)}: Detected language: {language_name} (confidence: {confidence:.2f})")
                
                # Prepare texts to fit within token limits
                truncated_cv, truncated_job = TextProcessor.prepare_for_llm(
                    self.cv, 
                    application,
                    max_total_chars=5000  # Approximately 1250 tokens, well under 6000 limit
                )
                
                # Generate a structured letter using the model with language parameter
                letter: CoverLetterSchema = chain.invoke({
                    "cv": truncated_cv,
                    "job_description": truncated_job,
                    "language": language_name
                })

                # Save or handle the generated letter
                letter_manager.manage(letter.title, letter.content)

                # Store the result
                results.append(letter)
                print(f"✅ Cover letter generated in {language_name}")
            except Exception as e:
                print(f"❌ Error generating letter: {e}")
                continue

        return results