import os
import sys
import logging

from typing import Dict, Optional
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.append(project_root)

from src.utils.file_handler import FileHandler
from src.utils.text_processor import TextProcessor
from src.api.openai.client import OpenAIClient
from src.services.key_words.key_words_extractor import KeyWordsGenerator


class MetadataBuilder:
    
    def __init__(self, llm_system_prompt_path: str):
        self.file_handler = FileHandler()
        self.keywords_generator = KeyWordsGenerator(llm_system_prompt_path)

    @staticmethod
    def get_metadata(file_name: str, text: str, keywords: list) -> dict:
        """
        Generates dictionary containig metadata.
        
        Parameters:
            file_name (str) : Name of the file
            text (str) : Contect of the text
            keywords (List[str]) : List of the keywords generated for text

        Return :
            Dict[str : str] : Dictionary containing metadata
        """
        file_metadata = {
            "filename":file_name,
            "text": text,
            "keywords":keywords
        }
        return file_metadata
    
    def generate_files_metadata(self, directory_path: str) -> list[Dict]:
        """
        Generates metadata for all files in the specified directory.

        Parameters:
            directory_path (str): Path to direcotry containing files to process

        Returns:
            list[Dict]: List of metadata dictionaries for each file, where each dictionary contains:
                - filename: name of the file
                - text: content of the file
                -keywords: list of generated keywords for the file content
        
        Example return structure:
        [
            {
                'filename' : 'file1.txt',
                'text' : 'Content of file 1 ...',
                'keywords' : ['keyword1', 'keyword2', 'keyword3' ...]
            },
            ...
        ]
        """
        metadata_list = []

        # get all files paths from directory
        files = self.file_handler.get_list_file_paths_from_direcotry(directory_path, ['.txt'])
        logging.info(f"Found {len(files)} files to process")

        for file_path in files:
            try:
                logging.info(f"Processing file: {Path(file_path).name}")
                text_content = self.file_handler.load_txt(file_path)

                # Generate keywords for file content
                keywords = self.keywords_generator.generate_keywords(file_path)
                logging.info(f"Generated {len(keywords)} keywords for {Path(file_path).name}")

                # Create metadata object from file
                file_metadata = self.get_metadata(
                    file_name=Path(file_path).name,
                    text=text_content,
                    keywords=keywords
                )
                metadata_list.append(file_metadata)

            except Exception as e:
                logging.error(f"Error processing {file_path}: {str(e)}")
                # Adding empty metadata to maintain file order
                file_metadata = self.get_metadata(
                    file_name=Path(file_path).name, 
                    text = text_content,
                    keywords=[]
                )
                metadata_list.append(file_metadata)
        
        return metadata_list
    
    def save_metadata_as_json(self, metadata_list: list, destination_path: str="tasks", file_name: str ="default.json") -> None:
        """
        Save metadata list of dictionaries as JSON file with given name and under given location.
        
        Parameters:
            metadata_list (list[dict[str:str]]) : List of metadata dictionaries for each processed file
            destination_path (str) : destination path to saving file
            file_name (str): Name under which file will be saved

        Returns:
            None
        """
        filename_path = os.path.join(destination_path,file_name)
        self.file_handler.save_json(filename_path, metadata_list)
    

    


    