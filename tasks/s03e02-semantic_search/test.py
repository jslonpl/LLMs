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

from src.api.qdrant.client import QdrantClient
from src.api.qdrant.point_struct_generator import PointStructBuilder
from src.api.openai.client import OpenAIClient
from src.api.aidevs3.uploader import Uploader

def qdrant_test():
    qdrant_client = QdrantClient()
    collection_name = "s03e02"
    #qdrant_clinet.create_collections(collection_name, 1536)

    collection = qdrant_client.list_collections()
    collection_info = qdrant_client.get_collection(collection_name)
    print(collection_info)

def embedding_test():
    clinet_openai = OpenAIClient()
    embedding = clinet_openai.generate_embedding("Hello World")
    print("Embedding vector number of elements : ",len(embedding))

    # Sprawdź typy elementów w liście
    if all(isinstance(x, int) for x in embedding):
        print("Embedding jest listą liczb całkowitych (int).")
    elif all(isinstance(x, str) for x in embedding):
        print("Embedding jest listą łańcuchów znaków (str).")
    elif all(isinstance(x, float) for x in embedding):
        print("Embedding jest listą liczb zmiennoprzecinkowych (float).")
    else:
        print("Embedding zawiera mieszane lub nieznane typy danych.")


def generating_point():
    point_builder = PointStructBuilder("tasks/s03e02-semantic_search/llm_system_prompt.txt")
    points = point_builder.get_points_from_dict("tasks/s03e02-semantic_search/test")
    point_builder.save_points_as_JSON(points, "tasks/s03e02-semantic_search/test")


def insert_data_to_collection():
    collection_name = "s03e02"

    qdrant_client = QdrantClient()
    point_builder = PointStructBuilder("tasks/s03e02-semantic_search/llm_system_prompt.txt")
    points = point_builder.get_points_from_dict("files/pliki_z_fabryki/do-not-share")
    qdrant_client.upsert_points(collection_name, points)

def qdrant_search():
    openai_clinet = OpenAIClient()
    qdrant_client = QdrantClient()
    collection_name = "s03e02"
    question = "W raporcie, z którego dnia znajduje się wzmianka o kradzieży prototypu broni?"
    embedding_question = openai_clinet.generate_embedding(question)

    answer = qdrant_client.search_points(
        collection_name= collection_name, 
        query_vector=embedding_question, 
        limit=1
    )
    filename = answer[0]["payload"]["filename"]
    data = filename.removesuffix('.txt')
    return data.replace("_", '-')

def sent_data_to_aidevs3():
    taskname = "wektory"
    uploader = Uploader(taskname)

    data = qdrant_search()
    uploader.send_data(data)


def main():
    sent_data_to_aidevs3()

if __name__ == "__main__":
    main()