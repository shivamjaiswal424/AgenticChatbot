import os
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input=user_controls_input

    def get_llm_model(self):
        groq_api_key=self.user_controls_input.get("GROQ_API_KEY","").strip()
        selected_groq_model=self.user_controls_input.get("selected_groq_model","").strip()

        if not groq_api_key:
            raise ValueError("Groq API key is missing. Please enter it in the sidebar.")

        try:
            llm=ChatGroq(api_key=groq_api_key, model=selected_groq_model, temperature=0)
            llm.invoke("test")
        except Exception as e:
            error=str(e).lower()
            if "invalid api key" in error or "authentication" in error or "401" in error:
                raise ValueError("Invalid Groq API key. Please check and re-enter it in the sidebar.")
            if "model_not_found" in error or "does not exist" in error or "404" in error:
                raise ValueError(f"Model '{selected_groq_model}' not found on Groq. Try 'llama-3.3-70b-versatile' or check console.groq.com for available models.")
            raise ValueError(f"Failed to initialise Groq model: {e}")
        return llm

        

