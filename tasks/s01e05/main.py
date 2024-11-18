import os
import sys
import logging

# Get the absolute path to the root directory of your project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the project root to sys.path
sys.path.append(project_root)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from src.api.aidevs3.downloader import Downloader
from src.api.aidevs3.uploader import Uploader
from src.api.openai.client import OpenAIClient


def main():
    filename = "cenzura.txt"
    taskname = "CENZURA"
    downloader = Downloader(filename)
    uploader = Uploader(taskname)
    text_to_censore = downloader.get_file_txt()
    client = OpenAIClient()

    prompt = f"Replace the personal data with word CENZURA. Do not change the phrase structure. <Example>Input:Nazywam się James Bond. Mieszkam w Warszawie na ulicy Pięknej 5, Mam 28 lat. Output:Nazywam się CENZURA. Mieszkam w CENZURA na ulicy CENZURA. Mam CENZURA lat.</Example>{text_to_censore}"

    censored_text = client.generate_response(
        prompt,
        model= "gpt-3.5-turbo-0125",
        max_tokens=100
    )
    
    print(censored_text)
    uploader.send_data(censored_text)
    
    print(censored_text)




if __name__ == "__main__":
    main()
