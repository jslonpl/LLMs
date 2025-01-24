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

def solution():
    taskname = "softo"
    uploader = Uploader(taskname)

    answer = {
        "01" : "kontakt@softoai.whatever",
        "02": "https://banan.ag3nts.org/",
        "03": " ISO 9001 oraz ISO/IEC 27001"
    }
    r = uploader.send_data_as_conversation(answer)
    #print(r)

solution()