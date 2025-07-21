from langchain.prompts import PromptTemplate


"""A class to encapsulate various prompts used for LLMs."""
class Prompt:
    GENERATE_MOTIVATION = PromptTemplate.from_template(
        """
        You generate motivation letter with those informations : {informations}.  
        """
    )
