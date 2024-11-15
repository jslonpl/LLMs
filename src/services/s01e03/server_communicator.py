import logging
import requests
from config.settings import Config


class Aidevs3ServerCommunicator:
    """
    Handles communcation with the remote server.
    """

    def __init__(self):
        # use the Config class to get the URL and API key
        self.url = Config.get_key("ANSWER_URL")
        self.api_key = Config.get_key("AI_DEVS_3_API_KEY")

        # Check if the required configuration is available
        if not self.url or not self.api_key:
            logging.error(f"Aidevs3ServerCommunicator: Missing URL or API key in configuration.")
            raise ValueError("Missing configuration for Aidevs3ServerCommunicator")
        
    
    def send_data(self, task, data):
        """
        Send data to the server via POST request.

            Args:
                taks (str): The task identifier.
                data (dict): The data to send.

            Returns:
            dict: The server's response data if successful, None otherwise
        """
        payload = {
            "task": task,
            "apikey": self.api_key,
            "answer": data
        }
        try:
            response = requests.post(self.url, json=payload)
            if response.status_code == 200:
                response_data = response.json()
                logging.info(f"Server response: {response_data}")
                return response_data
            else:
                logging.error(f"Server returned status cpde {response.status_code}: {response.text}")
                return None
        except Exception as e:
            logging.error(f"Error sending data fo server: {e}")
            return None
    