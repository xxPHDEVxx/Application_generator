import warnings
from pathlib import Path
import pdfplumber
from config import CV_PATH, DESTINATION_PATH
from tools.scraper import Scraper
from utils.simple_pdf_generator import SimplePDFGenerator

# Suppress FontBBox warnings
warnings.filterwarnings('ignore', message='.*FontBBox.*')
warnings.filterwarnings('ignore', message='.*Could get FontBBox.*')


class PdfManager:
    """
    Extracts and returns the full text content from a PDF CV file.
    """

    def __init__(self, file_path=None):
        """
        Initialize the PDF manager.
        
        Args:
            file_path (str, optional): Path to the PDF file. Falls back to CV_PATH from config.
        """
        self.file = file_path or CV_PATH

    def run(self) -> str:
        """
        Opens the CV PDF and extracts text from all pages.

        Returns:
            str: The extracted text content of the PDF.
        """
        content = ""

        # Open the PDF file using pdfplumber
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with pdfplumber.open(self.file) as file:
                for page in file.pages:
                    # Extract text with adjusted tolerance for better layout preservation
                    txt = page.extract_text(x_tolerance=1.5, y_tolerance=2)
                    if txt:
                        content += txt + '\n'
        return content


class CoverLetterManager:
    """
    Manages the saving of generated cover letters into professional PDF files.
    """

    def __init__(self, destination_path=None):
        """
        Initialize the cover letter manager.
        
        Args:
            destination_path (str, optional): Path to save PDFs. Falls back to DESTINATION_PATH from config.
        """
        self.path = destination_path or DESTINATION_PATH
        Path(self.path).mkdir(parents=True, exist_ok=True)
        self.pdf_generator = SimplePDFGenerator()

    def manage(self, title: str, content: str) -> str:
        """
        Saves the given letter content to a professional PDF file.

        Args:
            title (str): The title of the letter (used as filename and document title).
            content (str): The content/body of the letter.

        Returns:
            str: The full path to the saved PDF file.
        """
        # Sanitize title for safe file naming
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).rstrip()
        filename = f"{safe_title}"
        full_path = Path(self.path) / filename
        
        # Generate PDF
        pdf_path = self.pdf_generator.generate_pdf(title, content, full_path)
        print(f"✅ Cover letter saved as: {pdf_path}")
        return str(pdf_path)


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
