from langchain.prompts import PromptTemplate


"""A class to encapsulate various prompts used for LLMs."""
class Prompt:
    GENERATE_MOTIVATION = PromptTemplate.from_template(
        """
        You are an assistant that generates structured cover letters.

        Based on the provided CV : {cv} and job description {job_description}, return a CoverLetterSchema
        """
    )
