import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class Models:
    MISTRAL = ChatGroq(model=os.getenv("MODEL"))
        