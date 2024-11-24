import os
import sys
from pathlib import Path
import logging
from typing import List, Tuple, Optional

# Add project root to Python path
project_root = str(Path(__file__).resolve().parent.parent.parent)
sys.path.append(project_root)

from src.api.openai.client import OpenAIClient
from src.services.speech_to_text.stt import WhisperModel, STTService
from src.utils.file_handler import FileHandler
from src.utils.text_processor import TextProcessor

logging.basicConfig(level=logging.INFO)


class FileManager:
    def __init__(self, directory_path:str , llm_system_prompt_path:str, vlm_system_prompt_path:str):
        self.directory_path = directory_path
        self.clinet_openai = OpenAIClient()
        self.handler = FileHandler()
        self.whisper_model = WhisperModel()
        self.stt_service = STTService(self.whisper_model)
        self.text_processor = TextProcessor()
        self.llm_system_prompt = self.handler.load_txt(llm_system_prompt_path)
        self.vlm_system_prompt = self.handler.load_txt(vlm_system_prompt_path)

    
    def process_files_in_direcotry(self) -> Tuple[List[str], List[str]]:
        # Action definition for each file type
        actions = {
            ".txt": self.process_txt_file,
            ".png": self.process_image_file,
            ".mp3": self.process_audio_file,
        }
        
        # Initialization lists to store file names by category
        people = []
        hardware = []

        # Get only files from the main direcotry (no subdirectories)
        for file in os.listdir(self.directory_path):
            # create full file path
            file_path = os.path.join(self.directory_path, file)

            # Skip if it's direcotry
            if os.path.isdir(file_path):
                logging.info(f"Skipping directory: {file}")
                continue

            # Get file extension
            file_extension = os.path.splitext(file)[1].lower()

            # Check if the file extension has a defined action
            if file_extension in actions:
                detected, category = actions[file_extension](file_path)
                if detected:
                    if category == "people":
                        people.append(file)
                    elif category == "hardware":
                        hardware.append(file)
                else:
                    logging.info(f"File: {file} does not matcg any target category.")
            else:
                logging.info(f"Skipping file: {file}")
        
        people.sort()
        hardware.sort()
        return people, hardware

    def process_audio_file(self, file_path: str) -> tuple[bool, Optional[str]]:
        transcription = self.stt_service.transcription(file_path, language='en')
        text = transcription["text"]
        logging.info(f"Transcription content: {text}")
        resp = self.process_llm(text)
        logging.info(f"LLM Response content: {resp}")
        return self.check_category(resp)

    
    def process_image_file(self, file_path:str) -> tuple[bool, Optional[str]]:
        image_description = self.process_vlm(file_path)
        resp = self.process_llm(image_description)
        logging.info(f"LLM Response content: {resp}")
        return self.check_category(resp)
    
    def process_txt_file(self,file_path: str) -> tuple[bool, Optional[str]]:
        text = self.handler.load_txt(file_path)
        logging.info(f"Text file. Text content: {text}")
        resp = self.process_llm(text)
        logging.info(f"LLM Response content: {resp}")
        return self.check_category(resp)

    @staticmethod
    def check_category(category:str):
        target_words = {"people", "hardware"}
        if category in target_words:
            return True, category
        else:
            return False, None
        
    def process_vlm(self, file_path: str) -> str:
        """ Return image description in str format. """
        vlm_description = self.clinet_openai.generate_visual_resposne(
            prompt=self.vlm_system_prompt,
            model="gpt-4o",
            image_path=file_path, 
            max_tokens=2000, temperature=1.0, 
            top_p=1.0
        )
        logging.info(f"VLM description: {vlm_description}")
        return vlm_description

    def process_llm(self, text:str) -> str:
        """ Return file content category : people, hardware, other. """
        llm_resp = self.clinet_openai.generate_response(
            system_prompt=self.llm_system_prompt,
            message=text,
            model="gpt-4o",
            max_tokens=2000,
            temperature=1.0,
            top_p=1.0
        )
        logging.info(f"LLM response: {llm_resp}")
        resp = self.text_processor.extract_text_between_tags(llm_resp, "answer")
        return resp
