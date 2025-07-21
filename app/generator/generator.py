from utils.prompts import Prompt
from utils.models import Models
from tools.file_manager import PdfManager

class Generator:
    def __init__(self, application: str):
        self.model = Models.MISTRAL
        self.prompt = Prompt.GENERATE_MOTIVATION
        self.application = application
        self.cv = PdfManager().run()

    def run(self):
        chain = self.prompt | self.model
        return chain.invoke({
            "cv": self.cv,
            "job_description": self.application
    }).content
