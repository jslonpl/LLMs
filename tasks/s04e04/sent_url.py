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


def sent_url():
    taskname = "webhook"
    uploader = Uploader(taskname)

    answer = "https://5ab7-83-4-64-113.ngrok-free.app/test_api"
    r = uploader.send_data_as_conversation(answer)
    #print(r)

sent_url()