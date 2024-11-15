import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import requests
from bs4 import BeautifulSoup
from src.api.openai_api import OpenAIClient



def get_human_question(url):
    # execution of post request
    response = requests.post(url)

    # checking wheather the query was performed correctly
    if response.status_code == 200:
        # parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # finding 'human-question' id element
        human_question = soup.find(id='human-question')

        if human_question:
            # Extracting text from element
            question_text = human_question.get_text(strip=True)
            cleaned_question = question_text.replace("Question:", "").strip()
            print(f"Pytanie weryfikacyjne: {cleaned_question}")
            return cleaned_question
        else:
            print("Nie znaleziono elementu 'human-question'.")
    else:
        print(f"Request error: {response.status_code}")

def post_answer_url(url):
    url_address = url
    question = get_human_question(url_address)
    print(question)
    
    client = OpenAIClient()
    model_response = client.generate_response(prompt=str(question), model='gpt-4', max_tokens=100)
    print(model_response)

    payload = {
        "username": "tester",
        "password": "574e112a",
        "answer": model_response
    }
    headers = {
    "Content-Type": "application/json"
    }

    response = requests.post(url_address, data=payload)

    print("Status code:", response.status_code)
    print("Odpowiedź:", response.text)

if __name__ == "__main__":
    url = "https://xyz.ag3nts.org/"
    post_answer_url(url)
