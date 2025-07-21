from langchain.prompts import PromptTemplate


"""A class to encapsulate various prompts used for LLMs."""
class Prompt:
    GENERATE_MOTIVATION = PromptTemplate.from_template(
        """
        You are an expert in writing cover letters. Based on the content of this cv : {cv}  and this job description {job_description}, write a professional, well-structured cover letter tailored to the position. The letter must be written in the language of the job description. Do not include any explanations, disclaimers, or additional commentary.

        Format your response strictly as follows:

        Title: [Title of the letter – e.g., Application for the position of Software Developer]

        Text:
        [Full cover letter text – including a compelling introduction, a structured body highlighting skills, experience, and motivation, and a polite closing.]

        """
    )
