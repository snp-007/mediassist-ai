from groq import Groq
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()


class GroqLLM:

    def __init__(self):

        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            api_key = os.getenv("GROQ_API_KEY")

        self.client = Groq(
            api_key=api_key
        )

        self.model = "llama-3.3-70b-versatile"

    def generate(
        self,
        prompt
    ):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        return response.choices[0].message.content