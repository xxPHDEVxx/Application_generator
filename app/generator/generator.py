from utils.prompts import Prompt
from utils.models import Models
from tools.file_manager import PdfManager

class Generator:
    def __init__(self):
        self.model = Models.MISTRAL
        self.prompt = Prompt.GENERATE_MOTIVATION
        self.cv = PdfManager().run()

    def run(self, applications):
        chain = self.prompt | self.model.with_structured_output()
        for application in applications:
            letter = chain.invoke({
            "cv": self.cv,
            "job_description": application
            }).content
        
