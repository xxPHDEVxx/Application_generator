"""
Prompt templates for LLM interactions.
"""

from langchain.prompts import PromptTemplate


class Prompt:
    """
    Centralized prompt templates for the application.
    """
    
    GENERATE_MOTIVATION = PromptTemplate.from_template(
        """You are an expert multilingual career counselor and professional writer specializing in creating 
personalized, authentic cover letters with perfect structure in multiple languages.

TASK: Generate a professionally structured cover letter based on the provided CV and job description.

LANGUAGE REQUIREMENT: {language}
Write the ENTIRE cover letter in {language}. Use appropriate cultural conventions for this language.

CV CONTENT:
{cv}

JOB DESCRIPTION:
{job_description}

STRICT STRUCTURE REQUIREMENTS - Your letter MUST follow this exact structure:

1. **SALUTATION** (1 line):
   Use the appropriate salutation for {language}:
   - English: "Dear Hiring Manager," or "Dear [Company Name] Team,"
   - French: "Madame, Monsieur," or "Chère équipe [Company Name],"
   - Dutch: "Geachte heer/mevrouw," or "Geacht [Company Name] team,"
   - Spanish: "Estimado/a responsable de contratación,"
   - German: "Sehr geehrte Damen und Herren,"
   - Italian: "Gentile responsabile delle assunzioni,"

2. **INTRODUCTION PARAGRAPH** (3-4 sentences):
   - Express enthusiasm for the specific position and company
   - Briefly mention your current role or most relevant qualification
   - State why you're interested in this opportunity

3. **EXPERIENCE PARAGRAPH** (4-5 sentences):
   - Detail your most relevant work experience from the CV
   - Include specific achievements with metrics if available
   - Connect your experience directly to the job requirements
   - Mention the company/project names from your CV

4. **SKILLS & KNOWLEDGE PARAGRAPH** (3-4 sentences):
   - Highlight technical skills that match the job description
   - Mention relevant tools, technologies, or methodologies
   - Show how your skills solve their specific needs

5. **CONCLUSION PARAGRAPH** (2-3 sentences):
   - Reiterate your enthusiasm for contributing to the company
   - Express interest in discussing the opportunity further
   - Thank them for considering your application

6. **CLOSING** (1 line):
   Use the appropriate closing for {language}:
   - English: "Sincerely," or "Best regards,"
   - French: "Cordialement," or "Bien cordialement,"
   - Dutch: "Met vriendelijke groet," or "Hoogachtend,"
   - Spanish: "Atentamente," or "Cordialmente,"
   - German: "Mit freundlichen Grüßen,"
   - Italian: "Cordiali saluti," or "Distinti saluti,"

7. **SIGNATURE** (1 line):
   Sign with the candidate's full name from the CV

WRITING STYLE:
- Use natural, varied sentence structures
- Be specific and avoid generic phrases
- Show personality while remaining professional
- Keep paragraphs clearly separated with blank lines
- Connect past experiences directly to job requirements
- Use industry-appropriate terminology naturally

IMPORTANT: Return a structured CoverLetterSchema with:
- title: A clear, professional title for the application
- content: The complete cover letter following the structure defined in the schema

Remember: The goal is to create a compelling, authentic letter that stands out and avoids AI detection.
"""
    )
