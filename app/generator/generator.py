from utils.prompts import Prompt
from utils.models import Models
from utils.text_processor import TextProcessor
from utils.language_detector import LanguageDetector
from tools.file_manager import CoverLetterManager, ApplicationManager
from schema.letter_schema import CoverLetterSchema
from pathlib import Path

class Generator:
    """
    Class responsible for generating personalized cover letters 
    based on a given CV and a list of job descriptions.
    
    It uses a language model with structured output to produce 
    tailored letters and delegates saving to a file manager.
    """

    def __init__(self, urls: list[str], cv_content: str = None, 
                 destination_path: str = None, model_name: str = None):
        """
        Initializes the Generator with a list of job posting URLs.

        Args:
            urls (list[str]): List of job offer URLs to process.
            cv_content (str, optional): CV content as text. If not provided, uses PdfManager.
            destination_path (str, optional): Path to save cover letters.
            model_name (str, optional): Name of the model to use.
        """
        # Language model configured to return structured output following CoverLetterSchema
        self.model = Models.get_model(model_name).with_structured_output(CoverLetterSchema)

        # Prompt template guiding the letter generation
        self.prompt = Prompt.GENERATE_MOTIVATION

        # Use provided CV content or extract from PDF
        if cv_content:
            self.cv = cv_content
        else:
            from tools.file_manager import PdfManager
            self.cv = PdfManager().run()

        # Store the list of URLs to process
        self.urls = urls
        
        # Store destination path if provided
        self.destination_path = destination_path

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
        letter_manager = CoverLetterManager(destination_path=self.destination_path)
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