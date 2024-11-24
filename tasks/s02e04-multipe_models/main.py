import logging.config
import os
import sys
import logging
import json

# Get the absolute path to the root directory of your project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the project root to sys.path
sys.path.append(project_root)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from src.api.aidevs3.downloader import Downloader
from src.api.aidevs3.uploader import Uploader
from src.api.openai.client import OpenAIClient
from src.utils.file_handler import FileHandler
from src.utils.text_processor import TextProcessor
from file_manager import FileManager

def main():
    dir_path = "tasks/s02e04-multipe_models/pliki_z_fabryki"
    task_name = "kategorie"

    vision_prompt_path = "tasks/s02e04-multipe_models/prompts/vision_prompt.txt"
    llm_system_prompt_path = "tasks/s02e04-multipe_models/prompts/llm_system_prompt.txt"
    clinet_openai = OpenAIClient()
    handler = FileHandler()
    uploader = Uploader(task_name)
    file_manager = FileManager(dir_path, llm_system_prompt_path, vision_prompt_path)

    people, hardware = file_manager.process_files_in_direcotry()
    data = {
        "people":people,
        "hardware":hardware
    }
    uploader.send_data(data)

"""
    hardware = ['2024-11-12_report-13.png',
                '2024-11-12_report-15.png', 
                '2024-11-12_report-17.png'
                ]
    
    people = ['2024-11-12_report-00-sektor_C4.txt', 
              '2024-11-12_report-07-sektor_C4.txt',
              '2024-11-12_report-10-sektor-C1.mp3',
              ]
"""  



if __name__ == "__main__":
    main()