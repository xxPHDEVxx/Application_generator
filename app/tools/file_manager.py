import pdfplumber
import os
import textwrap
from dotenv import load_dotenv
from tools.scraper import Scraper

# Load environment variables from .env file
load_dotenv()


class PdfManager:
    """
    Extracts and returns the full text content from a PDF CV file.
    The file path is read from the CV_PATH environment variable.
    """

    def __init__(self):
        self.file = os.getenv("CV_PATH")

    def run(self) -> str:
        """
        Opens the CV PDF and extracts text from all pages.

        Returns:
            str: The extracted text content of the PDF.
        """
        content = ""

        # Open the PDF file using pdfplumber
        with pdfplumber.open(self.file) as file:
            for page in file.pages:
                # Extract text with adjusted tolerance for better layout preservation
                txt = page.extract_text(x_tolerance=1.5, y_tolerance=2)
                if txt:
                    content += txt + '\n'
        return content


class CoverLetterManager:
    """
    Manages the saving of generated cover letters into formatted text files.
    The destination path is defined by the DESTINATION_PATH environment variable.
    """

    def __init__(self):
        self.path = os.getenv("DESTINATION_PATH")
        if not self.path:
            raise ValueError("The DESTINATION_PATH environment variable is not set.")
        if not os.path.exists(self.path):
            os.makedirs(self.path, exist_ok=True)

    def manage(self, title: str, content: str) -> str:
        """
        Saves the given letter content to a .txt file using a cleaned version of the title.

        Args:
            title (str): The title of the letter (used as filename and heading).
            content (str): The content/body of the letter.

        Returns:
            str: The full path to the saved file.
        """
        # Sanitize title for safe file naming
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).rstrip()
        filename = f"{safe_title}.txt"
        full_path = os.path.join(self.path, filename)

        # Prepare formatted content
        formatted_lines = []
        line_width = 80  # Ideal width for reading in editors or terminal

        # Centered title and underline
        centered_title = title.center(line_width)
        underline = "-" * len(title)
        centered_underline = underline.center(line_width)

        formatted_lines.append(centered_title)
        formatted_lines.append(centered_underline)
        formatted_lines.append("")  # Blank line

        # Split and wrap each paragraph
        paragraphs = content.split("\n")
        for paragraph in paragraphs:
            if paragraph.strip():
                wrapped = textwrap.fill(paragraph.strip(), width=line_width)
                formatted_lines.append(wrapped)
                formatted_lines.append("")  # Blank line between paragraphs

        # Write to file
        with open(full_path, "w", encoding="utf-8") as file:
            file.write("\n".join(formatted_lines))

        return full_path


class ApplicationManager:
    """
    Responsible for retrieving job descriptions from a list of URLs using a scraper.
    """

    def __init__(self, urls: list[str]):
        self.urls = urls
        self.scraper = Scraper()
        self.applications = []

    def run(self) -> list[str]:
        """
        Fetches and extracts the main content from each URL provided.

        Returns:
            list[str]: A list of job descriptions (text content).
        """
        for url in self.urls:
            # Assumes that the first document contains the main job content
            documents = self.scraper.run(url)
            self.applications.append(documents[0].page_content)
        return self.applications
