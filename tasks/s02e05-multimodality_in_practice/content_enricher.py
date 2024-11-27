import os
import sys
import logging
from typing import List, Tuple, Optional, Dict
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).resolve().parent.parent.parent)
sys.path.append(project_root)

from src.api.openai.client import OpenAIClient
from src.utils.file_handler import FileHandler
from src.utils.parser_html import HTMLParser, MediaPlaceholder

logging.basicConfig(level=logging.INFO)

class ContentEnricher:
    """ Class responsible for enriching web content with AI-generated description of images and audio transcription """
    def __init__(self, 
                 llm_system_prompt_path: str, 
                 vlm_system_prompt_path: str,
                 web_content_path: str, 
                 images_path: str, 
                 dst_path: str):
        """ Initialize ContentEnricher with necessary paths and clients.
        Args:
            vlm_system_prompt_path : Path to VLM prompt file
            llm_system_prompt_path : Path to LLM prompt file
            web_content_path : Path to text file containg website HTML description
            images_path : Path fo directory containg images downloaded from website
        """
        self._validate_paths(
            llm_system_prompt_path,
            vlm_system_prompt_path,
            web_content_path,
            images_path, 
            dst_path
        )
        self.client_openai = OpenAIClient()
        self.handler = FileHandler()
        self.parser = HTMLParser()
        try:
            self.vlm_system_prompt = self.handler.load_txt(vlm_system_prompt_path)
            self.llm_system_prompt = self.handler.load_txt(llm_system_prompt_path)
            self.web_content_to_parse = self.handler.load_txt(web_content_path)
            self.images_path = images_path
            self.dst_path = dst_path
        except FileNotFoundError as e:
            logging.error(f"Failed to load required files: {e}")
            raise

    @staticmethod
    def _validate_paths(*paths: str) -> None:
        """ Validate that all provided path exists. """
        for path in paths:
            if not Path(path).exists():
                raise FileNotFoundError(f"Path does not exist: {path}")

    def process_vlm(self, file_path: str) -> str:
        """ Generate description for an image using Vision Language Model.
        Args:
            file_path : Path to the image

        Returns:
            str: AI-generated description of the image
        """
        vlm_description = self.client_openai.generate_visual_resposne(
            prompt=self.vlm_system_prompt,
            model="gpt-4o",
            image_path=file_path,
            max_tokens=2000,
            temperature=1.0,
            top_p=1.0
        )
        logging.info(f"VLM description: {vlm_description}")
        return vlm_description

    def parse_html_to_text(self) -> Tuple[str, dict, dict]:
        """ Converte HTML website code saved as .txt file into the text file containg only website content.  
        Returns:
            tuple: (parsed_content, images_data, audio_data)
                - parsed_content (str): website content as text
                - images_data (dict): dictionary containg list of image placeholders
                - audio_data (dict): dictionary containg list of audio placeholders
        """
        web_content = self.parser.parse_html_to_text(self.web_content_to_parse)
        images_list = self.parser.get_image_data()
        audio_list = self.parser.get_audio_data()
        return web_content, images_list, audio_list
    
    def processs_image_palceholder(self, image_data: Dict[str, MediaPlaceholder]) -> None:
        """ Process image placeholder - adding image description into placeholder ai_description pole in MediaPlaceholder object
        
        Args:
            image_data: Dictionatry of image placeholders where key is image name and value is MediaPlacehoder object
        """
        for image_name, placeholder in image_data.items():
            image_path = os.path.join(self.images_path, image_name)

            if os.path.exists(image_path):
                try:
                    vlm_response = self.process_vlm(image_path)
                    caption = placeholder.caption
                    description = f"Nazwa zdjęcia: {image_name}, podpis: {caption}, dokładny opis: {vlm_response}"
                    placeholder.ai_description = description
                    logging.info(f"Generated description for image: {image_name}")
                except Exception as e:
                    logging.error(f"Failed to process image {image_name}: {e}")
            else:
                logging.warning(f"Image file not found: {image_path}")

    
    def enrich_content(self) -> str:
        """ Process HTML content and replace image placeholders woth their descriptions
        
        Returns:
            str: Enriched content with image descriptions located in proper places in text

        Raises:
            ValueError: If HTML parsing fails
            RuntimeError: If content enrichment process fails
        """
    
        try:
        # Parse HTML content and get media data
            parsed_content, images_data, _ = self.parse_html_to_text()
            if not parsed_content:
                raise ValueError("Failed to parse HTML content - empty result")
            
            # Process images and generate descriptions
            self.processs_image_palceholder(images_data)

            # create replacements direcotry from processed images
            replacements = {
                placeholder.unique_id: placeholder.ai_description
                for placeholder in images_data.values()
                if placeholder.ai_description is not None
            }

            if not replacements and images_data:
                logging.warning(f"No image descriptions were generated despite images being present")
        
            # Replace placeholders woth descriptions
            enriched_content = self.parser.replace_media_placeholders(parsed_content, replacements)
            if not enriched_content:
                raise ValueError("Failed to generate enriched content - empty result")
            
            self.handler.save_txt(os.path.join(self.dst_path, "enriched_web_content.txt"), enriched_content)
            return enriched_content
        except Exception as e:
            logging.error(f"Content enrichment failed: {str(e)}")
            raise RuntimeError(f"Failed to enrich content: {str(e)}") from e


    

    





    

