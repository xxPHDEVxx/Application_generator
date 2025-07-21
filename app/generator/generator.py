from utils.prompts import Prompt
from utils.models import Models
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

        for application in applications:
            # Generate a structured letter using the model
            letter: CoverLetterSchema = chain.invoke({
                "cv": self.cv,
                "job_description": application
            })

            # Save or handle the generated letter
            letter_manager.manage(letter.title, letter.content)

            # Store the result
            results.append(letter)

        return results
