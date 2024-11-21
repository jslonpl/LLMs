import os
import sys
import logging
import json

# Get the absolute path to the root directory of your project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the project root to sys.path
sys.path.append(project_root)

from audio_transcription_manager import AudioTranscriptionManager
from src.api.aidevs3.uploader import Uploader
from src.api.openai.client import OpenAIClient
from src.utils.file_handler import FileHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    files_path = '/Users/jakub/Documents/aidevs3/repo/tasks/s02e01-stt/audio'
    transcription_path = '/Users/jakub/Documents/aidevs3/repo/tasks/s02e01-stt/transcription'
    prompt_path = '/Users/jakub/Documents/aidevs3/repo/tasks/s02e01-stt/prompr.txt'
    taks_name = "mp3"

    handler = FileHandler()
    manager = AudioTranscriptionManager()
    clinet_openai = OpenAIClient()
    client_aidevs3 = Uploader(taks_name)

    prompt = handler.load_txt(prompt_path)
    #print(prompt)

    for file_name in os.listdir(transcription_path):
        if file_name.endswith('.txt'):
            text_file_path = os.path.join(transcription_path, file_name)
            transcription = manager.load_transciption(text_file_path)
            message = prompt + transcription
            logging.info(f"Loaded transcription : file name: {file_name}\n")
            
            #openAI resposne will be in JSON string
            openai_response = clinet_openai.generate_response(
                message,
                model= 'gpt-4o',
                max_tokens=1000
            )
            print(openai_response)
            try:
                response_json = json.loads(str(openai_response))
                decision = response_json[0]["decision"]
                print(openai_response, type(openai_response), f"decision: {decision}")
                if decision == "1":
                    answer = response_json[0]["answer"]
                    print(answer)
                    client_aidevs3.send_data(answer)
                    break
            except json.JSONDecodeError:
                print("Response format is not correct JSON.")


if __name__ == "__main__":
     main()