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
from src.utils.file_handler import FileHandler


def query_secret_tasl():
    taskname = "database"

    uploader = Uploader(taskname)
    
    query_secret_task = "SELECT letter FROM correct_order WHERE letter REGEXP '^[A-Za-z]$' ORDER BY weight"

    results = uploader.send_data_to_db(query_secret_task)
    logging.info(f"{results}")

def save_to_csv(data: dict) -> None:
    handler = FileHandler()
    file_path = "files/pliki_z_fabryki/rdb/connections.csv"
    columns = ["user1_id", "user2_id"]
    handler.save_to_csv(file_path, data, columns)


def query_main_task():
    queries = ["show tables", "show create table "]
    tables_name = ['connections', 'correct_order', 'datacenters', 'users']
    taskname = "database"
    dc_ids = []
    
    uploader = Uploader(taskname)
    
    
    query = queries[1]+tables_name[0]
    query1 = "SELECT id, username FROM users"

    query2 = "Select user1_id, user2_id FROM connections"

    query3 = "SELECT manager FROM datacenters"

    query4 = """SELECT d.dc_id
                FROM datacenters d
                JOIN users u ON d.manager = u.id
                WHERE d.is_active = 1
                AND u.is_active = 0
                """
    
    response = uploader.send_data_to_db(query2)
    #logging.info(response)

    #save_to_csv(response)
    



query_main_task()