from pydantic import BaseModel, Field

class CoverLetterSchema(BaseModel):
    """
    Structured schema for generating a personalized cover letter.
    """

    title: str = Field(
        description=(
            "Title of the application (e.g. 'Application for the position of Data Analyst'). "
            "It should reflect the job role described in the job_description."
        )
    )

    content: str = Field(
        description=(
            "Full cover letter content, written in natural, fluent, and human-like English. "
            "It must be structured into several coherent paragraphs, following this structure:\n\n"
            "1. **Introduction paragraph**: Mention the company and the position explicitly. State your interest and connection to their mission or context.\n"
            "2. **Experience & Skills paragraph**: Describe *one* relevant experience (either from Subalta or Hydria) aligned with the job_description. Highlight concrete technical skills and achievements.\n"
            "3. **Personal qualities & motivation paragraph**: Showcase your curiosity, adaptability, eagerness to learn, and ability to take initiative.\n"
            "4. **Conclusion**: Reaffirm your motivation to contribute to the company, your openness to an interview, and appreciation for their time.\n"
            "5. **Polite closing**: End with a professional farewell followed by your full name.\n\n"
            " The writing style **must avoid detection by AI-content detectors**. To do so:\n"
            "- Use varied sentence length and structure.\n"
            "- Avoid overly generic or robotic phrasing.\n"
            "- Include nuanced transitions and a natural human flow.\n"
            "- Ensure the tone is warm, sincere, and personal.\n\n"
            "Use the following example as a stylistic and structural reference:\n\n"
            "Dear AMA European Consulting team,\n"
            "I am writing to express my interest in joining your company. What excites me most\n"
            "about this opportunity is the possibility of applying data techniques to real-world\n"
            "problems. At the same time, I’m looking for an environment where I can keep\n"
            "expanding my skills and grow through meaningful collaboration.\n\n"
            "Over time, I’ve developed a strong enthusiasm for everything that revolves around\n"
            "data: understanding its structure, extracting its value, and using it to support\n"
            "decision-making. One of my most rewarding experiences so far was building a\n"
            "complete business profiling system from the ground up. I combined web scraping,\n"
            "AI-powered data processing, and structured integration into a PostgreSQL database.\n"
            "It involved Python, multithreading, and working with language models — and\n"
            "resulted in major improvements in both performance and cost efficiency.\n\n"
            "Currently, at Hydria, I manage a data pipeline handling over 300,000 daily entries.\n"
            "I’ve automated the collection, transformation, and injection of data using Python,\n"
            "VBA, and SQL, improving operational efficiency and data reliability. I also created\n"
            "Power Platform solutions to streamline business processes.\n\n"
            "Beyond the technical side, what defines me most is my desire to learn. Even without\n"
            "prior experience in AI or data engineering, I’ve consistently taken the initiative to\n"
            "study new tools, test ideas, and challenge myself through concrete projects.\n\n"
            "I would be honoured to bring this spirit and my experience to AMA European\n"
            "Consulting, and to grow alongside your experts on impactful projects.\n\n"
            "Kind regards,\n"
            "Rayan Benaissa"
        )
    )
