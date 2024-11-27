import logging.config
import os
import sys
import logging
import json
from dotenv import load_dotenv

# Get the absolute path to the root directory of your project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the project root to sys.path
sys.path.append(project_root)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from src.api.aidevs3.uploader import Uploader
from src.api.aidevs3.downloader import Downloader
from src.utils.file_handler import FileHandler
from src.utils.parser_html import HTMLParser
from src.services.speech_to_text.stt import WhisperModel, STTService
from src.api.openai.client import OpenAIClient
from content_enricher import ContentEnricher

def mp3_transcription():
    model = WhisperModel(model_size="large")
    stt_service = STTService(model)

    voice_path = "tasks/s02e05-multimodality_in_practice/content/rafal_dyktafon.mp3"
    dst_path = "tasks/s02e05-multimodality_in_practice/content/rafal_dyktafon.txt"
    dst_path = "tasks/s02e05-multimodality_in_practice/content/rafal_dyktafon.txt"

    transcription = stt_service.transcription(voice_path)
    stt_service.save_transcription(transcription["text"],dst_path)

def download_images(parser):
    downloader = Downloader("a")
    dst_path = "tasks/s02e05-multimodality_in_practice/content/images"
    for image in parser.get_image_data().values():
        #print(image.src)
        image_dst_path = os.path.join(dst_path, image.name)
        downloader.download_and_save_image(image_dst_path, image.src)

def enrich_text():
    content_enricher = ContentEnricher(
        llm_system_prompt_path= "tasks/s02e05-multimodality_in_practice/prompts/llm_system_prompt.txt",
        vlm_system_prompt_path= "tasks/s02e05-multimodality_in_practice/prompts/vision_prompt.txt",
        web_content_path="tasks/s02e05-multimodality_in_practice/content/web_content_html.txt",
        images_path="tasks/s02e05-multimodality_in_practice/content/test_images",
        dst_path= "tasks/s02e05-multimodality_in_practice/content"
    )

    parsed_web_content, images_placeholders, audio_placeholders = content_enricher.parse_html_to_text()
    
    # Filling placeholder with photo description
    content_enricher.processs_image_palceholder(images_placeholders)

    enriched_text = content_enricher.enrich_content()

    print(images_placeholders)


def model_answer():
    handler = FileHandler()
    client_openai = OpenAIClient()
    llm_system_prompt= handler.load_txt("tasks/s02e05-multimodality_in_practice/prompts/llm_system_prompt.txt")
    questions = handler.load_txt("tasks/s02e05-multimodality_in_practice/content/questions.txt")
    enriched_web_content = handler.load_txt("tasks/s02e05-multimodality_in_practice/content/enriched_web_content.txt")
    message = enriched_web_content + questions
    resp = client_openai.generate_response(
        system_prompt=llm_system_prompt,
        message=message,
        model="gpt-4o",
        max_tokens=16384,
        temperature=1.0,
        top_p=1.0
    )
    print(resp)

def main():
    task_name = "arxiv"
    client_aidevs3 = Uploader(task_name)
    answer={
        "01":"Truskawka",
        "02":"Kraków",
        "03":"Chciał znaleźć hotel",
        "04":"Pizza Hawajska",
        "05":"Brave New World"
    }
    client_aidevs3.send_data(answer)


if __name__ == "__main__":
    main()
