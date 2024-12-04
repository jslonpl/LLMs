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

from src.services.key_words.metadata_builder import MetadataBuilder
from src.utils.file_handler import FileHandler
from src.api.aidevs3.uploader import Uploader

def create_metadata_json_facts_dir():
    metadata_builder = MetadataBuilder(llm_system_prompt_path="tasks/s03e01-key_words/llm_system_prompt.txt")

    texts_directory_path = "tasks/s03e01-key_words/pliki_z_fabryki"
    destination_directory = "tasks/s03e01-key_words/content"
    file_name = "reports.json"

    metadata_list = metadata_builder.generate_files_metadata(texts_directory_path)
    metadata_builder.save_metadata_as_json(metadata_list,destination_directory, file_name)


def cross_reference_keywords():

    """
    
    Metoda do poprawy - nie działa do końca poprawnie.
    
    """
    reports_json_path = "tasks/s03e01-key_words/content/reports.json"
    facts_json_path = "tasks/s03e01-key_words/content/facts.json"
    
    file_handler = FileHandler()

    reports = file_handler.load_json(reports_json_path)
    facts = file_handler.load_json(facts_json_path)

    # Create a mapping of keywords to their full keyword lists from facts
    keyword_to_full_list = {}
    for fact in facts:
        for keyword in fact['keywords']:
            keyword_to_full_list[keyword.lower()] = fact['keywords']

    # Process each report
    for report in reports:
        matched_keywords = set()  # Using set to avoid duplicates
        
        # Check each report keyword against facts keywords
        for report_keyword in report['keywords']:
            report_keyword_lower = report_keyword.lower()
            if report_keyword_lower in keyword_to_full_list:
                # Add all keywords from the matching fact
                matched_keywords.update(keyword_to_full_list[report_keyword_lower])
        
        # Update report keywords with matched keywords
        report['keywords'] = list(set(report['keywords']) | matched_keywords)

    file_handler.save_json("tasks/s03e01-key_words/content/final.json", report)

def analyze_final_json():
    """
    Analyzes final.json and returns a dictionary with filenames and keys and comma-separated keywords as values
    """
    file_handler = FileHandler()
    final_json_path = "tasks/s03e01-key_words/content/final.json"

    # load the json file
    reports = file_handler.load_json(final_json_path)

    # create the result dictionary
    result = {}

    # process each report
    for report in reports:
        filename = report["filename"]
        # Joiin keywords with commas
        keywords_string = ", ".join(report["keywords"])
        result[filename] = keywords_string
    
    #print(result)
    return result
    

def main():
    taskname = "dokumenty"
    uploader = Uploader(taskname)

    uploader.send_data(analyze_final_json())
    


if __name__ == "__main__":
    main()