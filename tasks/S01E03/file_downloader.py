import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import logging
import requests
from config.settings import Config

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileDownloader:
    """ Class for configuration API and generating resposne. """
    def __init__(self):
        self.aidevs3_api_key = Config.get_key('AI_DEVS_3_API_KEY')

        if not self.aidevs3_api_key:
            raise ValueError('Missing AI_DEVS_3_API_KEY')
        
        self.request_url = f'https://centrala.ag3nts.org/data/{str(self.aidevs3_api_key)}/json.txt'

    
    def get_file_txt(self):
        # Downloading file
        response = requests.get(self.request_url)

        # Checked if download is executed
        if response.status_code == 200:
            # Saving JSON 
            with open('data.json', 'w', encoding='utf-8') as file:
                file.write(response.text)
            print("File saved as 'data.json' .")
        else:
            print(f'Error during downloading file: {response.status_code}')
