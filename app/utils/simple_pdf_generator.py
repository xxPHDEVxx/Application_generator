"""
Simple PDF generation for cover letters using FPDF (fallback solution).
"""

from pathlib import Path
from datetime import datetime
import textwrap

try:
    from fpdf import FPDF
    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False
    
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


class SimplePDFGenerator:
    """
    Generates PDF cover letters with a simple fallback to HTML if PDF libraries are not available.
    """
    
    def generate_pdf(self, title: str, content: str, output_path: Path) -> Path:
        """
        Generate a PDF or HTML file based on available libraries.
        
        Args:
            title: The title of the position
            content: The cover letter content
            output_path: Path where the file should be saved
            
        Returns:
            Path: The path to the generated file
        """
        if HAS_REPORTLAB:
            return self._generate_reportlab_pdf(title, content, output_path)
        elif HAS_FPDF:
            return self._generate_fpdf_pdf(title, content, output_path)
        else:
            return self._generate_html(title, content, output_path)
    
    def _generate_html(self, title: str, content: str, output_path: Path) -> Path:
        """
        Generate an HTML file as a fallback when PDF libraries are not available.
        """
        html_filename = output_path.with_suffix('.html')
        
        # Parse content into paragraphs
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
        
        # Build HTML content
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @media print {{
            body {{ margin: 0; }}
            .container {{ padding: 20px; }}
        }}
        body {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #000;
            background: white;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
            background: white;
        }}
        h1 {{
            font-size: 20px;
            text-align: center;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        .date {{
            color: #333;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        .salutation {{
            margin-bottom: 15px;
            font-size: 14px;
        }}
        p {{
            margin-bottom: 15px;
            text-align: justify;
            font-size: 14px;
            line-height: 1.8;
        }}
        .closing {{
            margin-top: 30px;
            margin-bottom: 5px;
            font-size: 14px;
        }}
        .signature {{
            font-weight: bold;
            font-size: 14px;
            margin-top: 30px;
        }}
        @page {{
            size: A4;
            margin: 2cm;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="date">{datetime.now().strftime("%B %d, %Y")}</div>
"""
        
        # Process paragraphs
        for i, para in enumerate(paragraphs):
            para_lower = para.lower()
            
            if para_lower.startswith(('dear', 'to whom')):
                html_content += f'        <div class="salutation">{para}</div>\n'
            elif any(word in para_lower for word in ['sincerely', 'regards', 'best', 'respectfully']):
                html_content += f'        <div class="closing">{para}</div>\n'
            elif i == len(paragraphs) - 1 and len(para) < 50:
                html_content += f'        <div class="signature">{para}</div>\n'
            else:
                html_content += f'        <p>{para}</p>\n'
        
        html_content += """    </div>
    <script>
        // Automatically offer to print as PDF when opened
        window.onload = function() {
            if (window.location.protocol === 'file:') {
                setTimeout(() => {
                    if (confirm('Would you like to save this as a PDF? Click OK to open the print dialog, then choose "Save as PDF".')) {
                        window.print();
                    }
                }, 500);
            }
        }
    </script>
</body>
</html>"""
        
        # Write HTML file
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_filename
    
    def _generate_reportlab_pdf(self, title: str, content: str, output_path: Path) -> Path:
        """Generate PDF using reportlab if available."""
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
        from reportlab.lib.colors import HexColor
        
        pdf_filename = output_path.with_suffix('.pdf')
        doc = SimpleDocTemplate(
            str(pdf_filename),
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=HexColor('#000000'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'BodyText',
            parent=styles['Normal'],
            fontSize=11,
            textColor=HexColor('#000000'),
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16,
            fontName='Helvetica'
        )
        
        story = []
        
        # Add title
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Add date
        date_text = datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(date_text, styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Add content paragraphs
        paragraphs = content.split('\n')
        for para_text in paragraphs:
            if para_text.strip():
                para = Paragraph(para_text.strip(), body_style)
                story.append(para)
                story.append(Spacer(1, 0.1 * inch))
        
        doc.build(story)
        return pdf_filename
    
    def _generate_fpdf_pdf(self, title: str, content: str, output_path: Path) -> Path:
        """Generate PDF using FPDF if available."""
        from fpdf import FPDF
        
        pdf_filename = output_path.with_suffix('.pdf')
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(25, 25, 25)
        
        # Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, title, 0, 1, 'C')
        pdf.ln(5)
        
        # Date
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 10, datetime.now().strftime("%B %d, %Y"), 0, 1, 'L')
        pdf.ln(10)
        
        # Content
        pdf.set_font("Arial", '', 11)
        paragraphs = content.split('\n')
        for para in paragraphs:
            if para.strip():
                # Wrap text
                lines = textwrap.wrap(para.strip(), width=80)
                for line in lines:
                    pdf.cell(0, 6, line, 0, 1)
                pdf.ln(3)
        
        pdf.output(str(pdf_filename))
        return pdf_filename