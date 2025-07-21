from utils.prompts import Prompt
from utils.models import Models


class Generator:
    def __init__(self, application: str):
        self.model = Models.MISTRAL
        self.prompt = Prompt.GENERATE_MOTIVATION
        self.application = application

    def run(self):
        chain = self.model | self.prompt
        return chain.invoke(
            self.application
            )