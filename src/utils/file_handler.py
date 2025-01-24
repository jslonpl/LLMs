import json
import logging
import base64
import imghdr
from pathlib import Path
import csv

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
    - save to csv

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

    @staticmethod
    def get_list_file_paths_from_direcotry(directory_path: str, file_extensions: list[str] = None) -> list[str]:
        """
        Gets list of full file paths for files from specific directory.

        Parameters:
            directory_path (str): Path to directory to scan
            file_extensions (List[str], Optional): List of file extension to filter (e.g. ['.txt', '.png', '.mp3', '.doc'])
                                                    If None -> returns all files path

        Returns:
            List[str]: List of fill file paths

        Raises:
            FileNotFoundError: If directory doesn't exist
            PermissionError: If no access to directory
        """
        try:
            # Convert string path to Path object
            dir_path = Path(directory_path)

            if not dir_path.exists():
                raise FileNotFoundError(f"Directory not found: {directory_path}")
            
            if not dir_path.is_dir():
                raise NotADirectoryError(f"Path is not a directory: {directory_path}")
            
            # Get all files from directory
            if file_extensions:
                # If extensions specified, filter files
                files = [
                    str(file.absolute())
                    for file in dir_path.iterdir()
                    if file.is_file() and file.suffix.lower() in file_extensions
                ]
            else:
                # If no extensions specified, get all files
                files = [
                    str(file.absolute())
                    for file in dir_path.iterdir()
                    if file.is_file()
                ]
            logging.info(f"Successfully retrieved {len(files)} files form {directory_path}")
            return files
        
        except PermissionError as pe:
            logging.error(f"Permission denied when accessing direcotry: {directory_path}")
            raise
        except Exception as e:
            logging.error(f"Error occured while scanning direcory {directory_path}: {e}")
            raise
    
    @staticmethod
    def save_to_csv(file_path: str, data: dict, columns: list[str]) -> None:
        """
        Save dictrionary to a CSV file with specified columns.

        Parameters:
            file_path (str): Path where to save the CSV file
            data (dict): Dictionary containing list of records to save
            columns (list[str]): List of column names to extract from each record

        Example:
            data = {'reply': [{'id': '1', 'username': 'Adrian'}, {'id': '2', 'username': 'Monika'}]}
            columns = ['id', 'username']
            save_to_csv('users.csv', data, columns)
        """
        try:
            records = data.get('reply', [])

            with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                # write header
                writer.writerow(columns)
                # write data rows
                for record in records:
                    row = [record.get(col, '') for col in columns]
                    writer.writerow(row)

            logging.info(f"Successfully saved CSV file: {file_path}")

        except Exception as e:
            logging.error(f"Error occurred during saving CSV file: {e}")
            raise

    
    @staticmethod
    def load_csv(file_path: str, as_dict: bool = True) -> list:
        """
        Load data from a CSV file.

        Parameters:
            file_path (str): Path to the cvs file
            as_dict (bool): If true, returns list of dictionaries, if False returns list

        Returns:
            list: List of records (euther dictionaries or lists depending on as_dict parameter)

        Example:
            # As dictionary
            data = load_csv('users.csv') # Returns: [{'id': '1', 'username': 'Adrian'}, ...]
            # As list
            data = load_csv('users.csv, as_dict=False) # Returns: [['1', 'Adrian'], ...]
        """
        try:
            with open(file_path, 'r', encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file)
                # Read Headers
                headers = next(csv_reader)

                if as_dict:
                    data = [dict(zip(headers, row)) for row in csv_reader]
                else:
                    data = [row for row in csv_reader]
            logging.info(f"Successfully loaded CSV file: {file_path}")
            return data
        
        except FileNotFoundError:
            logging.error(f"CSV file not found! Check path {file_path}")
            raise
        except Exception as e:
            logging.error(f"Error occured during loading CSV file: {e}")
            raise
        

