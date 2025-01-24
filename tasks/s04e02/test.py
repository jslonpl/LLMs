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

def create_data_for_tunning():
    data_txt_path = 'files/pliki_z_fabryki/lab_data/correct.txt'
    data_jsonl_path = 'tasks/s04e02/tunning.jsonl'

    logging.info(f"Starting conversion from {data_txt_path} to {data_jsonl_path}")

    try:
        # Read the input file and create the JSONL file
        with open(data_txt_path, 'r') as input_file, \
            open(data_jsonl_path, 'a') as output_file:

            lines_processed = 0
            for line in input_file:
                # Remove any whitespace / newlines
                numbers = line.strip()
                # Create the complete structure
                json_line = {
                    "messages": [
                        {"role": "system", "content": "validate numbers"},
                        {"role": "user", "content": numbers},
                        {"role": "assistant", "content": "1"}
                    ]
                }
                # Converting to JSON string and write to file
                output_file.write(json.dumps(json_line) + "\n")
                lines_processed += 1
            
            logging.info(f"Successfully processed {lines_processed} lines.")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except Exception as e:
        logging.error(f"An error occures: {e}")
    
    logging.info("Conversion completed.")

def solution():
    taskname = "research"
    uploader = Uploader(taskname)

    answer = ["01", "02", "10"]
    r = uploader.send_data_as_conversation(answer)
    #print(r)

solution()