import os
import sys

# Get the absolute path to the root directory of your project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Add the project root to sys.path
sys.path.append(project_root)

import requests
import logging
import json
from config.settings import Config

class Uploader:
    """
    Class responsible for sending response to server

    :param task_name: - Name of the taks
    :param data: - Data to sent to the server
    """

    def __init__(self, taks_name: str):
        self.task_name = taks_name
        self.aidevs3_api_key = Config.get_key('AI_DEVS_3_API_KEY')

        if not self.aidevs3_api_key:
            raise ValueError("Missing 'AI_DEVS_3_API_KEY'.")
        
        self.response_request_url = f"https://centrala.ag3nts.org/report"

    
    def send_data(self, data) -> bool:
        """
        Send response to the server

        :return: True if sending was successful, Otherwise False
        """
        print(self.aidevs3_api_key)
        payload = {
            "task": str(self.task_name),
            "apikey": str(self.aidevs3_api_key),
            "answer": str(data)
        }
        

        data = json.dumps(payload, ensure_ascii=False)
        print(data)

        try:
            response = requests.post(self.response_request_url, json=payload)
            response.raise_for_status()
            response_data = response.json()
            logging.info("Data was sent successfully.")
            logging.info(f"Server response: {response_data}")
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during sending data: {e} , resp status_code: {response.status_code} : {response.text}")
            return False
