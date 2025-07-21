import pdfplumber
import os
import textwrap
from dotenv import load_dotenv
from tools.scraper import Scraper
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

    def manage(self, title: str, content: str) -> str:
        """
        Creates a .txt file named after the provided title in the destination path.

        Args:
            title (str): The title (used as filename and centered heading).
            content (str): The body of the cover letter.

        Returns:
            str: Full path to the created file.
        """
        # Nettoyer le titre pour le nom de fichier
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).rstrip()
        filename = f"{safe_title}.txt"
        full_path = os.path.join(self.path, filename)

        # Préparation du contenu formaté
        formatted_lines = []

        # Centrer le titre
        line_width = 80  # Largeur idéale pour lecture sur terminal ou éditeur
        centered_title = title.center(line_width)
        underline = "-" * len(title)
        centered_underline = underline.center(line_width)

        formatted_lines.append(centered_title)
        formatted_lines.append(centered_underline)
        formatted_lines.append("")  # Ligne vide

        # Découper le texte en paragraphes et reformater
        paragraphs = content.split("\n")
        for paragraph in paragraphs:
            if paragraph.strip():
                wrapped = textwrap.fill(paragraph.strip(), width=line_width)
                formatted_lines.append(wrapped)
                formatted_lines.append("")  # Ligne vide après chaque paragraphe

        # Écriture dans le fichier
        with open(full_path, "w", encoding="utf-8") as file:
            file.write("\n".join(formatted_lines))

        return full_path
    
class ApplicationManager:
    def __init__(self, urls: list[str]):
        self.urls = urls
        self.scraper = Scraper()
        self.applications = []

    def run(self):
        for url in self.urls:
            documents = self.scraper.run(url)
            self.applications.append(documents[0].page_content)
        return self.applications
