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


def query_secret_tasl():
    taskname = "database"

    uploader = Uploader(taskname)
    
    query_secret_task = "SELECT letter FROM correct_order WHERE letter REGEXP '^[A-Za-z]$' ORDER BY weight"

    results = uploader.send_data_to_db(query_secret_task)
    logging.info(f"{results}")


def query_main_task():
    queries = ["show tables", "show create table "]
    tables_name = ['connections', 'correct_order', 'datacenters', 'users']
    taskname = "database"
    dc_ids = []
    
    uploader = Uploader(taskname)
    
    query = queries[1]+tables_name[3]
    query1 = "SELECT dc_id FROM datacenters WHERE is_active = 0"
    query2 = "Select user1_id, user2_id FROM connections"
    query3 = "SELECT manager FROM datacenters"
    query4 = """SELECT d.dc_id
                FROM datacenters d
                JOIN users u ON d.manager = u.id
                WHERE d.is_active = 1
                AND u.is_active = 0
                """


    response = uploader.send_data_to_db(query4)
    #logging.info(response)

    
    db_result = response.get('reply')
    logging.info(f"Server resposne - db_ids: {db_result}")

    for item in db_result:
        logging.info(item)
        dc_id = item['dc_id']
        dc_ids.append(dc_id)
    
    dc_ids.sort(key=int)
    
    logging.info(f"List of datacenter ids: {dc_ids}")

    final_response = uploader.send_data_to_central(dc_ids)
    if not final_response:
        logging.error("Failed to send final answer")
    



query_main_task()