import os
import sys
from pathlib import Path
import logging
import json

# Get the absolute path to the project root directory
project_root = Path(__file__).resolve().parents[2]

# Add the project root to sys.path
sys.path.append(str(project_root))
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from src.api.aidevs3.uploader import Uploader
from src.api.aidevs3.downloader import Downloader
from src.utils.file_handler import FileHandler

def get_questions():
    downloader = Downloader("notes.json")
    handler = FileHandler()

    json_save_path = "tasks/s04e05/questions.json"

    json_data = downloader.get_file_json()
    handler.save_json(json_save_path, json_data)


def solution():
    taskname = "notes"
    uploader = Uploader(taskname)

    answer = {
        "01" : "2019",
        "02": "Adam",
        "03": "Jaskinia",
        "04": "2024-11-12",
        "05": "Do Lubawy koło Grudziądza"
    }
    r = uploader.send_data_as_conversation(answer)
    #print(r)

solution()