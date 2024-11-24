import json
import logging
import base64
import imghdr
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileHandler():
    """
    Class allow to sava and read files , ex. '.txt', '.json' 

    Main functionalities:
    - read text from disc (.txt)
    - save text files to disc (.txt)
    - read JSON files from disc (.json)
    - save JSON files to disc (.json)
    - load image and return its base64 encoded string

    Usage exampe:
    handler = FileHandler()
    content = handler.read_txt('example.txt')
    handler.write_json('data.json, {'key':'value'})
    """
    @staticmethod
    def load_txt(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                logging.info(f"Successfully loaded file from path: {file_path}")
                return content
        except FileNotFoundError:
            logging.error(f"Text file not found! Check path : {file_path}")
            raise
        except Exception as e:
            logging.error(f"Error occured during loading content from file: {e}")
            raise

    @staticmethod
    def save_txt(file_path: str, content: str) -> None:
        try:
            with open(file_path, 'w', encoding='utf') as file:
                file.write(content)
                logging.info(f"Successfully saved text file: {file_path}")
        except Exception as e:
            logging.error(f"Error occured during saving text file: {e}")
            raise

    @staticmethod
    def load_json(file_path: str) -> dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logging.info(f"Successfully loaded JSON file: {file_path}")
                return data
        except FileNotFoundError:
            logging.error(f"JSON file not found! Check path: {file_path}")
            raise
        except json.JSONDecodeError:
            logging.error(f"JSON decoding error in file: {file_path}")
            raise
        except Exception as e:
            logging.error(f"Error occured during loading content from file: {e}")

    @staticmethod
    def save_json(file_path: str, data: dict) -> None:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                logging.info(f"Successfully saved JSON file: {file_path}")
        except Exception as e:
            logging.error(f"Error occured during saving JSON file: {e}")

    @staticmethod
    def load_image_base64(file_path: str) -> str:
        """
        Loads an image and returns its base64 encoded string.

        Params:
            file_path (str): Path to the image file

        Returns:
            str: Base64 encoded image string
        """
        try:
            if not Path(file_path).is_file():
                raise FileNotFoundError(f"Image file not found at path: {file_path}")
            
            image_format = imghdr.what(file_path)
            supported_formats = ['jpeg', 'png', 'gif', 'bmp']
            if not image_format or image_format.lower() not in supported_formats:
                raise ValueError(f"Unsupported image format: {image_format}")
            
            with open(file_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

            # Mapowanie formatu obrazu na typ MIME
            mime_type = f"image/{'jpeg' if image_format == 'jpeg' else image_format}"
            data_url = f"data:{mime_type};base64,{encoded_image}"
            
            logging.info(f"Successfully loaded and encoded image: {file_path}")
            return data_url
        
        except FileNotFoundError as e:
            logging.error(f"Image file not found: {e}")
            raise
        except ValueError as e:
            logging.error(f"Invalid image format: {e}")
            raise
        except Exception as e:
            logging.error(f"Error occurred during image processing: {e}")
            raise
