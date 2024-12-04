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

class KeyWordsGenerator:
    def __init__(self, llm_system_prompt_path: str):
        """
        Initialization of class

        Parameters:
            client_openai : client OpenAI
            handler : instance of FileHandler
            text_path (str) : Path to the analysed text file
            llm_prompt_path (str) : Path to the llm system prompt control key words generation
        """
        self.client_openai = OpenAIClient()
        self.handler = FileHandler()
        self.text_processor = TextProcessor()
        self.llm_system_prompt = self.handler.load_txt(llm_system_prompt_path)

    @staticmethod
    def check_keyword(keyword: str, keywords_list: list) -> bool:
        """
        Check if the keyword exists in the keywords list.

        Parameters:
            keyword (str): The keyword to check
            keywords_list (List[str]) : List of existing keywords

        Returns:
            bool: True if keyword exists in keywords_list, False otherwise
        """
        return keyword.lower() in [word.lower() for word in keywords_list]
    
    def llm_reponse(self, text: str) -> str:
        resposne = self.client_openai.generate_response(
            system_prompt=self.llm_system_prompt,
            message=text,
            model="gpt-4o",
            max_tokens=1000,
            temperature=1.0,
            top_p=1.0
        )
        return resposne

    def process_keywords_from_text(self, text: str, keywords_list: list) -> list:
        """
        Process text to extract and validate keywords against existing keywords list.

        Parameters:
            text (str): Text containing potential keywords
            existing_keywords(List[str]): List of existing keywords

        Returns:
            List[str]: Updated list of keywords
        """

        words = self.text_processor.tokenize_text(text)

        for word in words:
            if not self.check_keyword(word, keywords_list):
                keywords_list.append(word)
        
        return keywords_list


    def generate_keywords(self, text_path):
        """
        Generate list of key words for given text.

        Returns:
            List [str] : List of key words
        """
        try:
            # Initializaiton of keywords_list
            keywords_list = []

            text = self.handler.load_txt(text_path)
            text_chanks = self.text_processor.split_text_into_chanks(text, "\n")
            
            # Check if text is "entry deleted" first
            if self.text_processor.check_text_contain(text.strip(), "entry deleted"):
                return keywords_list

            for paragraph in text_chanks:
                try:
                    llm_response = self.llm_reponse(paragraph)
                    logging.info(f"LLm response for text {paragraph}:\n{llm_response}")
                    keywords_text = self.text_processor.extract_text_between_tags(llm_response, "keywords")
                    keywords_list = self.process_keywords_from_text(keywords_text, keywords_list)
                except Exception as e:
                    logging.error(f"Error processing paragraph in {text_path} : {str(e)}")
                    continue

            return keywords_list
        
        except FileNotFoundError as e:
            logging.error(f"File not found at {self.text_path}: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Error generating keywords: {str(e)}")
            return keywords_list


        
                    

    
                




