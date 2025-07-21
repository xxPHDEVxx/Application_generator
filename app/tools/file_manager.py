import pdfplumber
import os
from dotenv import load_dotenv
load_dotenv()


class PdfManager:
    """
        return the content of the cv (pdf file)
    """
    def __init__(self):
        self.file = os.getenv("CV_PATH")

    def run(self):
        content = ""

        with pdfplumber.open(self.file) as file:
            for page in file.pages:
                txt = page.extract_text(x_tolerance=1.5, y_tolerance=2)
                if txt:
                    content += txt + '\n'
        return content