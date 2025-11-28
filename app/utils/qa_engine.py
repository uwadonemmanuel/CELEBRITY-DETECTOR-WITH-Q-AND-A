import os
import requests
import logging

logger = logging.getLogger(__name__)

class QAEngine:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.error("GROQ_API_KEY environment variable is not set!")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        # Using a currently available Groq model for text generation
        # llama-3.1-70b-versatile has been decommissioned, using llama-3.1-8b-instant instead
        self.model  = "llama-3.1-8b-instant"

    def ask_about_celebrity(self,name,question):
        headers = {
            "Authorization" : f"Bearer {self.api_key}",
            "Content-Type" : "application/json"
        }

        prompt = f"""
                    You are a AI Assistant that knows a lot about celebrities. You have to answer questions about {name} concisely and accurately.
                    Question : {question}
                    """
        
        payload  = {
            "model" : self.model,
            "messages" : [{"role" : "user" , "content" : prompt}],
            "temperature" :  0.5,
            "max_tokens" : 512
        }

        if not self.api_key:
            logger.error("GROQ_API_KEY is not set. Cannot make API call.")
            return "Error: GROQ_API_KEY is not configured. Please set it in your environment variables."

        try:
            response = requests.post(self.api_url , headers=headers , json=payload, timeout=30)

            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                error_msg = f"API request failed with status {response.status_code}: {response.text}"
                logger.error(error_msg)
                return f"Sorry, I couldn't find the answer. Error: {error_msg}"
        
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            return f"Sorry, I encountered a network error: {error_msg}"
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return f"Sorry, an unexpected error occurred: {error_msg}"



