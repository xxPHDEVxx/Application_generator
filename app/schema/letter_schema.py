from typing import List
from pydantic import BaseModel, Field


class CoverLetterSchema(BaseModel):
    """
    Schema for encapsulating the cover letter.
    """
    title: str = Field(description="Application title.")
    content: List[str] = Field(description="Cover letter content")