import logging.config
import os
import sys
import logging
import json
from dotenv import load_dotenv
import re
from pathlib import Path

# Get the absolute path to the root directory of your project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the project root to sys.path
sys.path.append(project_root)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


from src.api.openai.client import OpenAIClient
from src.api.aidevs3.uploader import Uploader
from src.api.aidevs3.downloader import Downloader

def test():
    uploader = Uploader("loop")
    
    answer = "ELBLAG"

    uploader.send_data_to_central(answer)


test()