import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.append(project_root)

import logging
import requests
from src.api.aidevs3.client import Aidevs3Client

# Logging configuration
logging.basicConfig(level=logging.INFO)

class Downloader:
    """ Class for download file """
    def __init__(self, filename: str):
        self.filename = filename
        self.client = Aidevs3Client()
        self.api_key = self.client.get_api_key()
        self.data_url = self.client.get_data_url()
        self.dane_url = self.client.get_dane_url()
        self.request_url = f"{self.data_url}/{self.api_key}/{self.filename}"

    
    def download_file_txt(self, save_path:str ="data.json"):
        """ 
        Download file from url and save it to file on disc. 
        
        :return: True if download was successful
        """
        try:
            response = requests.get(self.request_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during download file: {e}")
            return False
        
        try:
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
                logging.info("File downloaded succesfully, saved as 'data.json' .")
                return True
        except IOError as e:
            logging.error(f"Error during saving file: {e}")
            return False
        

    def get_file_json(self):
        """
        Download data from URL and return as a JSON.

        :return: Dict representig JSON data or None if error occurs.
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

        :return: Dict representig TXT data or None if error occurs.
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


    def get_webpage_content(self, url:str ):
        """
        Download webpage content from given URL.

        :param url: URL of webpage to download
        :return : Touple containing (status_code, headers, content) or (None, None, None)
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            logging.info(f"Successfully downloaded content from {url}")
            return (
                response.status_code,
                dict(response.headers),
                response.text
            )
        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading webpage {url, {e}}")
            return None, None, None
        
    
    def download_and_save_image(self, save_path: str = None, image_url: str = None) -> bool:
        """
        Download image from aidevs3 server and save it to disc.

        Args:
            save_path: Path where to save the image

        Returns:
            bool: True if download was successful, False otherwise
        """
        try:
            request_url = os.path.join(self.dane_url, image_url)
            response = requests.get(request_url)
            response.raise_for_status()

            # Ensure that saving direcotry exists
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else ".", exist_ok=True)

            # Save the image
            with open(save_path, "wb") as file:
                file.write(response.content)
                logging.info(f"Image downloaded successfully, saved as '{save_path}'")
                return True
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Error durin image download: {e}")
            return False
        except IOError as e:
            logging.error(f"Error saving image: {e}")
            return False



        
    
        