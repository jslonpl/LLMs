import os
import requests
from dotenv import load_dotenv


class OpenAIClient:
    def __init__(self):
        load_dotenv()
        self.api_key = self._get_env_var("OPEN_AI_API_KEY")
        self.base_url = 'https://api.openai.com/v1'

    def _get_env_var(self, var_name: str) -> str:
        value = os.getenv(var_name)
        if not value:
            raise ValueError(f"Environment variable {var_name} is not set.")
        return value

    def _headers(self):
        # Returns authorization headers required for communication with the OpenAI API
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    def generate_response(self, prompt, model='gpt-4', max_tokens=50):
        # Returns model response based on prompt for selected model
        url = f"{self.base_url}/chat/completions" # FUlly endpoint to response generation
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        }

        response = requests.post(url, headers=self._headers(), json=payload)

        # Error handling
        if response.status_code != 200:
            self._handle_error(response)

        response_data = response.json()
        return response_data.get("choices", [])[0].get("message", {}).get("content", "")
    

    def _handle_error(self, resposne):
        ### Handles HTTP errors and displays error details ###
        try:
            error_data = resposne.json()
            error_message = error_data.get("error", {}).get("message", "Unknown error")
        except ValueError:
            error_message = "Communication with OpenAI error."

        raise Exception(f"API Error ({resposne.status_code}): {error_message}")