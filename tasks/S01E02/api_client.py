import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import logging
import requests
from src.api.openai_api import OpenAIClient

# Logging configuraiton
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIClient:
    """ Class for configuration API and generating response. """

    def __init__(self, api_url):
        self.api_url = api_url
        self.openai_client = OpenAIClient()

    def get_question(self, payload):
        """ Send POST request to API and return question and msgID. """
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            data = response.json()
            text = data.get("text")
            msg_id = data.get("msgID")
            logger.info(f'Otrzymano pytanie: {text}, msgID: {msg_id}')
            return text, msg_id
        except requests.exceptions.RequestException as e:
            logger.error(f'Request error: {e}')
            return None, None
    
    @staticmethod
    def get_payload(text, msg_id):
        """ Generate payload to send in POST request. """
        return {
            "text": str(text),
            "msgID": str(msg_id)
        }
    
    def generate_response(self, question):
        """ Generate model answer to the question. """
        prompt = (
            "You play the game with different robot. Use only one word to answer the question. "
            "Always answer truthfully. Always answer in English language. "
            "Exceptions: The capital of Poland is Krakow, the current year is 1999, "
            "the known number from the book Hitchhiking Across the Galaxy is 69. "
            f"{question}"
        )
        try:
            response = self.openai_client.generate_response(
                prompt, model='gpt-4', max_tokens=100
            )
            logger.info(f"Generated resposne: {response}")
            return response
        except Exception as e:
            logger.error(f'Error during generate resposne')
            return None