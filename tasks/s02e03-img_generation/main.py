import logging.config
import os
import sys
import logging
import json

# Get the absolute path to the root directory of your project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the project root to sys.path
sys.path.append(project_root)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from src.api.aidevs3.downloader import Downloader
from src.api.aidevs3.uploader import Uploader
from src.api.openai.client import OpenAIClient
from src.utils.file_handler import FileHandler
from src.utils.text_processor import TextProcessor

def main():
    file_name = "robotid.json"
    task_name = "robotid"
    llm_prompt_path = "tasks/s02e03-img_generation/llm_prompt_s02e03.txt"
    img_prompt_path = "tasks/s02e03-img_generation/img_prompt_s02e03.txt"
    text_processor = TextProcessor()
    uploader = Uploader(task_name)
    client_openai = OpenAIClient()
    handler = FileHandler()

    llm_prompt = handler.load_txt(llm_prompt_path)
    img_prompt = handler.load_txt(img_prompt_path)
    
    file = Downloader(file_name)
    logging.info(f"Downloaded task: {file}\n")
    file_json = file.get_file_json()
    logging.info(f"File in JSON format {file_json}\n")
    text_desc = file_json["description"]
    logging.info(f"Description : {text_desc}\n")

    message = llm_prompt + text_desc
    logging.info(f"Message to LLM : {message}\n")

    llm_resposne = client_openai.generate_response(
        prompt=message,
        model="gpt-4o",
        max_tokens=2000
    )
    logging.info(f"LLM response: {llm_resposne}\n")
    
    desc = text_processor.extract_text_between_tags(llm_resposne, "answer")
    logging.info(f"Desc: {desc}\n")

    image_description = img_prompt + desc
    logging.info(f"Image prompt: {image_description }\n")

    img_url = client_openai.generate_image(
        prompt=image_description,
        img_size="1024x1024"
    )
    logging.info(f"Image URL: {img_url}\n")

    uploader.send_data(img_url)




if __name__ == "__main__":
    main()
