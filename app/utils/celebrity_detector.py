import os
import base64
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CelebrityDetector:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.error("GROQ_API_KEY environment variable is not set!")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        # Current Groq vision models (as of 2025):
        # - meta-llama/llama-4-maverick-17b-128e-instruct (powerful, large context)
        # - meta-llama/llama-4-scout-17b-16e-instruct (lighter, faster)
        # Llama 3.2 vision models were deprecated April 14, 2025
        self.models_to_try = [
            "meta-llama/llama-4-maverick-17b-128e-instruct",  # Primary: powerful vision model
            "meta-llama/llama-4-scout-17b-16e-instruct",      # Fallback: lighter vision model
        ]
        self.model = self.models_to_try[0]  # Start with first model

    def identify(self , image_bytes):
        encoded_image = base64.b64encode(image_bytes).decode()

        headers = {
            "Authorization" : f"Bearer {self.api_key}",
            "Content-Type" : "application/json"
        }

        prompt = {
            "model": self.model,
            "messages": [
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text",
                            "text": """You are a celebrity recognition expert AI. 
Identify the person in the image. If known, respond in this format:

- **Full Name**:
- **Profession**:
- **Nationality**:
- **Famous For**:
- **Top Achievements**:

If unknown, return "Unknown".
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.3,    
            "max_tokens": 1024     
        }


        if not self.api_key:
            logger.error("GROQ_API_KEY is not set. Cannot make API call.")
            return "Error: GROQ_API_KEY is not configured. Please set it in your environment variables.", ""

        # Try each model until one works
        last_error = None
        for model_name in self.models_to_try:
            prompt["model"] = model_name
            logger.info(f"Trying model: {model_name}")
            
            try:
                response = requests.post(self.api_url , headers=headers , json=prompt, timeout=30)

                if response.status_code == 200:
                    result = response.json()['choices'][0]['message']['content']
                    name = self.extract_name(result)
                    logger.info(f"Successfully identified celebrity: {name} using model {model_name}")
                    self.model = model_name  # Remember working model
                    return result , name  
                else:
                    error_data = response.json() if response.text else {}
                    error_code = error_data.get("error", {}).get("code", "")
                    
                    # If model is decommissioned, try next model
                    if error_code == "model_decommissioned" or "decommissioned" in response.text.lower():
                        logger.warning(f"Model {model_name} is decommissioned, trying next model...")
                        last_error = f"Model {model_name} decommissioned"
                        continue
                    else:
                        # Other errors, return immediately
                        error_msg = f"API request failed with status {response.status_code}: {response.text}"
                        logger.error(error_msg)
                        return f"Error: {error_msg}", ""
            
            except requests.exceptions.RequestException as e:
                error_msg = f"Network error with {model_name}: {str(e)}"
                logger.warning(error_msg)
                last_error = error_msg
                continue
            except Exception as e:
                error_msg = f"Unexpected error with {model_name}: {str(e)}"
                logger.warning(error_msg)
                last_error = error_msg
                continue
        
        # All models failed
        error_msg = f"All models failed. Last error: {last_error}. Please check https://console.groq.com/docs/models for available vision-capable models."
        logger.error(error_msg)
        return f"Error: {error_msg}", ""  


    def extract_name(self,content):
        for line in content.splitlines():
            if line.lower().startswith("- **full name**:"):
                return line.split(":")[1].strip()

        return "Unknown"    


