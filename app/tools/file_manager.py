import pdfplumber
import os
from loguru import logger as logging
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
    

class CoverLetterManager:
    """
        location management for cover letters
    """
    def __init__(self):
        self.path = os.getenv("DESTINATION_PATH")
        if not self.path:
            raise ValueError("The DESTINATION_PATH environment variable is not set.")
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)

    def manage(self, title: str, content: str):
        """
        Creates a .txt file named after the provided title in the destination path.

        Args:
            title (str): The title (will be used as the filename).
            content (str): The content to write inside the file.

        Returns:
            str: Full path to the created file.
        """
        # Clean
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).rstrip()
        filename = f"{safe_title}.txt"
        full_path = os.path.join(self.path, filename)

        with open(full_path, "w", encoding="utf-8") as file:
            file.write(content)

        return full_path
