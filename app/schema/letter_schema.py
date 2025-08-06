from pydantic import BaseModel, Field

class CoverLetterSchema(BaseModel):
    """
    Structured schema for generating a personalized cover letter.
    """

    title: str = Field(
        description="Title of the application (e.g. 'Application for Data Analyst position')"
    )

    content: str = Field(
        description=(
            "Full cover letter content following a professional structure:\n"
            "1. Salutation (Dear...)\n"
            "2. Introduction paragraph - express interest and mention the position\n"
            "3. Experience paragraph - highlight relevant experience and achievements\n"
            "4. Skills paragraph - showcase technical skills and knowledge\n"
            "5. Conclusion paragraph - reiterate motivation and interest\n"
            "6. Professional closing (Sincerely, Regards, etc.)\n"
            "7. Full name signature\n\n"
            "The letter should be written in natural, professional language appropriate "
            "for the detected language of the job posting."
        )
    )