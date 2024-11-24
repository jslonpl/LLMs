import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.append(project_root)

import logging
import requests
import json
from src.api.aidevs3.client import Aidevs3Client

class Uploader:
    """
    Class responsible for sending response to server

    :param task_name: - Name of the taks
    :param data: - Data to sent to the server
    """

    def __init__(self, taks_name: str):
        self.task_name = taks_name
        self.client = Aidevs3Client()
        self.api_key = self.client.get_api_key()
        self.response_url = self.client.get_endpoint_url()

    def send_data(self, data) -> bool:
        """
        Send response to the server

        :return: True if sending was successful, Otherwise False
        """

        payload = {
            "task": str(self.task_name),
            "apikey": str(self.api_key),
            "answer": data
        }
        

        data = json.dumps(payload, ensure_ascii=False)
        print(data)

        try:
            response = requests.post(self.response_url, json=payload)
            response.raise_for_status()
            response_data = response.json()
            logging.info("Data was sent successfully.")
            logging.info(f"Server response: {response_data}")
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during sending data: {e} , resp status_code: {response.status_code} : {response.text}")
            return False

