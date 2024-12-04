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

from src.utils.file_handler import FileHandler
from src.utils.text_processor import TextProcessor
from src.services.key_words.key_words_extractor import KeyWordsGenerator
from src.services.key_words.metadata_builder import MetadataBuilder

texts = {
    "fact1" : "tasks/s03e01-key_words/pliki_z_fabryki/facts/f01.txt",
    "fact2" : "tasks/s03e01-key_words/pliki_z_fabryki/facts/f02.txt",
    "fact3" : "tasks/s03e01-key_words/pliki_z_fabryki/facts/f03.txt",
    "fact4" : "tasks/s03e01-key_words/pliki_z_fabryki/facts/f04.txt",
    "fact5" : "tasks/s03e01-key_words/pliki_z_fabryki/facts/f05.txt", 
    "fact6" : "tasks/s03e01-key_words/pliki_z_fabryki/facts/f06.txt",
    "fact7" : "tasks/s03e01-key_words/pliki_z_fabryki/facts/f07.txt",
    "fact8" : "tasks/s03e01-key_words/pliki_z_fabryki/facts/f08.txt",
    "fact9" : "tasks/s03e01-key_words/pliki_z_fabryki/facts/f09.txt",
    "rep1" : "tasks/s03e01-key_words/pliki_z_fabryki/2024-11-12_report-00-sektor_C4.txt",
    "rep2" : "tasks/s03e01-key_words/pliki_z_fabryki/2024-11-12_report-01-sektor_A1.txt",
    "rep3" : "tasks/s03e01-key_words/pliki_z_fabryki/2024-11-12_report-02-sektor_A3.txt",
    "rep4" : "tasks/s03e01-key_words/pliki_z_fabryki/2024-11-12_report-03-sektor_A3.txt",
    "rep5" : "tasks/s03e01-key_words/pliki_z_fabryki/2024-11-12_report-04-sektor_B2.txt",
    "rep6" : "tasks/s03e01-key_words/pliki_z_fabryki/2024-11-12_report-05-sektor_C1.txt",
    "rep7" : "tasks/s03e01-key_words/pliki_z_fabryki/2024-11-12_report-06-sektor_C2.txt",
    "rep8" : "tasks/s03e01-key_words/pliki_z_fabryki/2024-11-12_report-07-sektor_C4.txt",
    "rep9" : "tasks/s03e01-key_words/pliki_z_fabryki/2024-11-12_report-08-sektor_A1.txt",
    "rep10" : "tasks/s03e01-key_words/pliki_z_fabryki/2024-11-12_report-09-sektor_C2.txt"
    
}

def occurence_special_signs(dict):
    handler = FileHandler()
    path = dict["fact1"]
    text = handler.load_txt(path)

    special_signs = ['\n', # newline
                    '\t',  # horizontal tab
                    '\r',  # carriage return
                    '\v',  # vertical tab
                    '\f']   # form feed
    
    occurence = {}
    print(text)

    for sign in special_signs:
        quantity = text.count(sign)
        occurence[repr(sign)] = quantity

    print("Occurence special signs in text:")
    for sing, amount in occurence.items():
        print(f"{sing}: {amount}")

def chack_paragraphs_quantity(dict):
    handler = FileHandler()
    text_proc = TextProcessor()
    path = dict["rep9"]
    keywords_generator = KeyWordsGenerator(llm_system_prompt_path="tasks/s03e01-key_words/llm_system_prompt.txt")
    
    keywords = keywords_generator.generate_keywords(path)
    print(keywords)


def get_file_paths():
    dir_path = "tasks/s03e01-key_words/pliki_z_fabryki"
    handler = FileHandler()
    file_paths = handler.get_list_file_paths_from_direcotry(dir_path, ['.txt'])
    for file_path in file_paths:
        print(Path(file_path).name)

def test_metadata_builder():
    metadata_builder = MetadataBuilder(llm_system_prompt_path="tasks/s03e01-key_words/llm_system_prompt.txt")
    metadata_list = metadata_builder.generate_files_metadata("tasks/s03e01-key_words/content")
    metadata_builder.save_metadata_as_json(metadata_list, "tasks/s03e01-key_words/content", "test_metadata.json")


#chack_paragraphs_quantity(texts)
test_metadata_builder()