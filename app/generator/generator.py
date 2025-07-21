from utils.prompts import Prompt
from utils.models import Models
from tools.file_manager import *
from schema.letter_schema import CoverLetterSchema

class Generator:
    def __init__(self, urls: list[str]):
        self.model = Models.MISTRAL.with_structured_output(CoverLetterSchema)
        self.prompt = Prompt.GENERATE_MOTIVATION
        self.cv = PdfManager().run()
        self.urls = urls

    def run(self):
        chain = self.prompt | self.model
        letter_manager = CoverLetterManager()
        application_manager = ApplicationManager(self.urls)
        applications = application_manager.run()
        results = []
        for application in applications:
            letter : CoverLetterSchema = chain.invoke({
                "cv": self.cv,
                "job_description": application
            })
            letter_manager.manage(letter.title, letter.content)
            results.append(letter)
        return results
        
