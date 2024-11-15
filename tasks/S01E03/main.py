import os
import sys
import logging

# Get the absolute path to the root directory of your project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the project root to sys.path
sys.path.append(project_root)

from src.services.s01e03.data_processor import DataProcessor
from src.services.s01e03.server_communicator import Aidevs3ServerCommunicator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    input_file_path = 'tasks/S01E03/data.json'
    output_file_path = 'tasks/S01E03/cor_data.json'

    if not input_file_path or not output_file_path:
        logging.error("Main: Missing input or output file path.")
        return
    
    data_processor = DataProcessor(input_file_path, output_file_path)

    # load data from input file
    data_processor.load_json_data()

    # Process the loaded data
    data_processor.process_data()
    # Save the processed data to the output file
    data_processor.save_json_data()

    # send the processed data to the server


if __name__ == "__main__":
    main()