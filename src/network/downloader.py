import os
import sys

# Get the absolute path to the root directory of your project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Add the project root to sys.path
sys.path.append(project_root)

import logging
import requests
from config.settings import Config

# Logging configuration
logging.basicConfig(level=logging.INFO)

class Downloader:
    """ Class for download file """
    def __init__(self, filename:str ):
        self.filename = filename
        self.aidevs3_api_key = Config.get_key('AI_DEVS_3_API_KEY')
        
        if not self.aidevs3_api_key:
            raise ValueError("Missing 'AI_DEVS_3_API_KEY'.")
        
        self.request_url = f"https://centrala.ag3nts.org/data/{self.aidevs3_api_key}/{self.filename}"
    

    def download_file_txt(self):
        """
        Download file from url and save it to file on disc.

        return: True if download was successful
        """
        try:
            response = requests.get(self.request_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f" Error during download file: {e}")
            return False
        
        try:
            with open('data.json', 'w', encoding='utf-8') as file:
                file.write(response.text)
                logging.info("File downloaded succesfully, saved as 'data.json' .")
                return True
        except IOError as e:
            logging.error(f"Error during saving file: {e}")
            return False

        
    def get_file_json(self):
        """
        Download data from URL and return as a JSON.

        return: Dict representig JSON data or None if error occurs.
        """

        try:
            response = requests.get(self.request_url)
            print(self.request_url)
            response.raise_for_status()
            data = response.json()
            logging.info('Data downloaded successfully.')
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during downloading data: {e}")
            return None
        except ValueError as e:
            logging.error(f"Error during parse JSON data: {e}")
            return None
        
    
    def get_file_txt(self):
        """
        Download data from URL and return as a TXT.

        return: Dict representig TXT data or None if error occurs.
        """
        try:
            response = requests.get(self.request_url)
            response.raise_for_status()

            ## Printing headers and them values
            #for header, value in response.headers.items():
            #    logging.info(f"{header}: {value}")
            data = response.text
            logging.info(f"Data downloaded successfully.\n\n{data}")
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during downloading data: {e}")
            return None
