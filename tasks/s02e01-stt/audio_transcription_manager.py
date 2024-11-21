import os
import sys
from pathlib import Path

# Get the absolute path to the root directory of your project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the project root to sys.path
sys.path.append(project_root)

import logging
from src.services.speech_to_text.stt import STTService, WhisperModel
from src.utils.file_handler import FileHandler
# Logging configuration
logging.basicConfig(level=logging.INFO)

class AudioTranscriptionManager:
    def __init__(self):
        self.whisper_model = WhisperModel(model_size="base")
        self.stt_service = STTService(model=self.whisper_model)
        self.handler = FileHandler()

    def audio_to_text_save(self, audios_path:str, dest_path:str) -> None:
        for file_name in os.listdir(audios_path):
            # Checking audio files format:
            if file_name.endswith('.m4a'):
                file_path = os.path.join(audios_path, file_name)
                result = self.stt_service.transcription(file_path, language='pl')
                text = result["text"]
                logging.info(f"Audio {file_name} transcripted successfully. Text: {text}")

                # Construct the path for saving the transcription
                destination_transcription_path = os.path.join(dest_path, f"{os.path.splitext(file_name)[0]}.txt")

                # Saving transcription as '.txt' file
                self.stt_service.save_transcription(text, destination_transcription_path)

    def load_transciption(self, text_path: str) -> str:
        content = self.handler.load_txt(text_path)
        return content
    
    

    