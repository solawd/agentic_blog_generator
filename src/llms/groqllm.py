from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv

from groq import Groq


def get_available_models():
    # Initialize the Groq client with your API key
    # It's recommended to store your API key as an environment variable
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
    models = client.models.list()
    return models


class GroqLLM:
    def __init__(self):
        load_dotenv()


    def get_llm(self, model="llama-3.1-8b-instant", groq_api_key=''):
        try:
            if not groq_api_key:
                self.groq_api_key=os.getenv("GROQ_API_KEY")
            else:
                self.groq_api_key=groq_api_key
            llm=ChatGroq(api_key=self.groq_api_key,model=model)
            return llm
        except Exception as e:
            raise ValueError(f"Error occurred with exception : {e}")
