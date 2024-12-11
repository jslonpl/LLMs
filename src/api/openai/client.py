import os
import requests
from dotenv import load_dotenv
from src.utils.file_handler import FileHandler


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
    
    def generate_response(self, system_prompt: str="", message:str="", model:str='gpt-4', max_tokens:int=50, temperature:float=1.0, top_p:float=1.0):
        # Returns model response based on prompt for selected model
        url = f"{self.base_url}/chat/completions" # FUlly endpoint to response generation
        payload = {
            "model": model,
            "messages":[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p
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
    

    def generate_image(self, prompt: str, img_size:str="1024x1024") -> str:
        """ Generate an image besed on the provided prompt """
        url = f"{self.base_url}/images/generations"
        payload = {
            "prompt": prompt,
            "n": 1,
            "size": img_size
        }

        response = requests.post(url, headers=self._headers(), json=payload)

        # Error handling
        if response.status_code != 200:
            self._handle_error(response)

        response_data = response.json()
        return response_data.get("data", [])[0].get("url", "")
    

    def generate_visual_resposne(self, prompt: str, model: str = "gpt-4o", image_path: str = "", max_tokens: int=1000, temperature: float=1.0, top_p: float=1.0):
        """ Return model response based on prompt for gpt-4-visual model."""
        handler = FileHandler()
        base64_image = handler.load_image_base64(image_path)
        url = url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {
                    "role":"user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": base64_image
                            },
                        },
                    ],
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        }
        
        response = requests.post(url, headers=self._headers(), json=payload)

        # Error Handling
        if response.status_code != 200:
            self._handle_error(response)

        response_data = response.json()
        return response_data.get("choices", [])[0].get("message", {}).get("content", "")
    

    def generate_embedding(self, text: str, model: str = "text-embedding-3-small") -> list:
        """
        Generate embeddings for the given text using OpenAI's models.

        Parameters:
            text (str) : Text based on which embedding will be generated.
            model (str) : embedding model
        
        Returns:
            List[int] : List containing embedding vector

        Avalilable OpenAI'm embedding models:
            defalt : text-embedding-3-small
                     text-embedding-3-large
                     text-embedding-ada-002
        """
        url = f"{self.base_url}/embeddings"
        payload = {
            "model": model,
            "input": text
        }
        
        response = requests.post(url, headers=self._headers(), json=payload)

        if response.status_code != 200:
            self._handle_error(response)

        response_data = response.json()
        return response_data.get("data",[])[0].get("embedding",[])
