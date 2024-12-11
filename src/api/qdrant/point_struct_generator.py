import os
import sys
import logging

from typing import Dict, Optional, List
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.append(project_root)

from src.utils.file_handler import FileHandler
from src.utils.text_processor import TextProcessor
from src.api.openai.client import OpenAIClient
from src.services.key_words.key_words_extractor import KeyWordsGenerator
from qdrant_client import models
import uuid

class PointStructBuilder:
    def __init__(self, llm_system_prompt_path: str) -> None:
        self.file_handler = FileHandler()
        self.client_openai = OpenAIClient()
        self.keywords_generator = KeyWordsGenerator(llm_system_prompt_path)

    
    @staticmethod
    def generate_uuid() -> str:
        """
        Generates a unique UUID for a point

        Returns:
            str: A uniqie UUID string
        """
        return str(uuid.uuid4())
    
    def single_point_struct(self, filename:str, text:str, keywords: List[str], embedding: List[float]) -> Dict:
        """
        Generate point structure for given data.

        Parameters:
            filename (str) : Name of the file
            text (str) : Text content to be stored
            keywords(List[str]): List of keywords associated with the text
            embedding (List[float]): Vector embedding of the text

        Returns:
            model.PointStruct: Qdrant point structure containing the data 
        """

        # Validate input types
        if not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords):
            raise TypeError("keywords must be a list of strings")
        if not isinstance(embedding, list) or not all(isinstance(e, float) for e in embedding):
            raise TypeError("embedding must be a list of floats")
        point = models.PointStruct(
            id = self.generate_uuid(),
            payload = {
                "filename" : filename,
                "text": text,
                "keywords" : keywords,
                "category":"text",
            },
            vector = embedding,
        )
        return point
    

    def get_points_from_dict(self, dict_path: str) -> dict:
        points = []

        # Get all files path from directory
        files = self.file_handler.get_list_file_paths_from_direcotry(dict_path, ['.txt'])
        logging.info(f"Found {len(files)} files to process.")

        for file_path in files:
            try:
                logging.info(f"Processing file: {Path(file_path).name}")
                text_content = self.file_handler.load_txt(file_path)

                # Generate keywords from file content
                keywords = self.keywords_generator.generate_keywords(file_path)
                logging.info(f"Generated {len(keywords)} keywords for {Path(file_path).name}")

                # Create Embedding
                embedding = self.client_openai.generate_embedding(text_content)
                logging.info(f"Generated embedding, vector size: {len(embedding)}")

                # Create point_structure
                point = self.single_point_struct(
                    filename=str(Path(file_path).name),
                    text=text_content,
                    keywords=keywords,
                    embedding=embedding
                )
                logging.info(f"Generated point point structure\n{point}")

                points.append(point)

            except Exception as e:
                logging.error(f"Error processing {file_path}: {str(e)}")
                point = self.single_point_struct(
                    filename=str(Path(file_path).name),
                    text="Error processing file",
                    keywords=[],
                    embedding=[0.0]*1536
                )

        return points
    

    def save_points_as_JSON(self, points: list, dest_path: str, filename: str = "qdrant_test_point.json") -> None:
        """
        Save metadata list of dictionaries as JSON file with given name and under given location.
        
        Parameters:
            metadata_list (list[dict[str:str]]) : List of metadata dictionaries for each processed file
            dest_path (str) : destination path to saving file
            filename (str): Name under which file will be saved

        Returns:
            None
        """
        # Convert points to serializable format
        serializable_points = [
            {
                "id" : str(point.id),
                "payload": point.payload,
                "vector": point.vector
            }
            for point in points
        ]
        filename_path = os.path.join(dest_path, filename)
        self.file_handler.save_json(filename_path, serializable_points)






    

    


    
    


    
        

