from config.tasks.S01E03.file_downloader import FileDownloader
import json

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.api.openai_api import OpenAIClient
import requests


def openai_response(question):
    client = OpenAIClient()
    prompt = f"Use the shortest possibe phraze to answer.{question}"
    try:
        response = client.generate_response(
            prompt, model='gpt-4', max_tokens=50
        )
        return response
    except Exception as e:
        print(f'Error during generate response: {e}')
        return None

def save_to_json(output_file_path, data):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def check_calc(question, answer):
    if question and answer is not None:
        try:
            # calculations
            res = eval(question)
            if answer == res:
                print(f"Correct answer for question! '{question}' = {res}")
                return None
            else:
                print(f"INCORRECT answer for question '{question}' . There was : {answer} , EXPECTED: {res}")
                return res
        except Exception as e:
            print(f"Error during calculating question '{question}': {e}")
    else:
        print(f"No complete data in question...")

def route_calculation(data):
    no = 0
    for item in data.get("test-data", []):
        if "test" in item:
            question = item.get("test",{}).get("q")
            answer = item.get("test",{}).get("a")
            correct_anser = openai_response(question)
            item["test"]["a"] = correct_anser
            print(f'Question : {question}, answer: {answer}, model_resp: {correct_anser}')
        else:
            question = item.get("question")
            answer = item.get("answer")
            ans = check_calc(question, answer)
            if ans is not None:
                item["answer"] = ans



def check_answer():
    file_path = 'config/tasks/S01E03/data.json'
    corrected_file_path = 'config/tasks/S01E03/corrected_data.json'
    data = load_json(file_path)
    route_calculation(data)
    save_to_json(corrected_file_path, data)
    #print(data)


def sent_answer_to_server(data):
    answer_url = 'https://centrala.ag3nts.org/report'
    payload={
        "task": "JSON",
        "apikey": "7c51149e-f594-4a6f-9503-7420e771b9fb",
        "answer": data
    }
    server_response = requests.post(answer_url, json=payload)
    if server_response.status_code == 200:
        data = server_response.json()
        print(data)
    else:
        print(server_response.status_code, server_response.json())



def main():
    corrected_file_path = 'config/tasks/S01E03/corrected_data.json'
    data = load_json(corrected_file_path)
    sent_answer_to_server(data)
    #check_answer()
    #api_client = FileDownloader()
    #api_client.get_file_txt()


if __name__ == "__main__":
    main()