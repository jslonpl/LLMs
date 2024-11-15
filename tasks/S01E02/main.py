import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import requests
from src.api.openai_api import OpenAIClient

def get_question(url, payload):
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()

        text = data.get("text")
        msgID = data.get("msgID")

        print(text, type(text))
        print(msgID, type(msgID))
        return text, msgID
    else:
        print(f"Request error: {response.status_code}")
        return None, None

def get_payload(text, msgID):
    payload = {
        "text": str(text),
        "msgID": str(msgID)
    }
    return payload


def client_response(question):
    client = OpenAIClient()

    prompt = f"You play the game with different robot. Use only one word to answer the question. Always answer truthfully. Always answer in english language. Exceptions: The capital of Poland is Krakow, the current year is 1999, the known number from the book Hitchhiking Across the Galaxy is 69. {question}"
    
    response = client.generate_response(prompt, model="gpt-4", max_tokens=100)
    print(response)

    return response




if __name__ == "__main__":
    url = "https://xyz.ag3nts.org/verify"

    text, msgID = get_question(url, get_payload("READY", "0"))
    response = client_response(text)
    answer, msgID_resp = get_question(url, get_payload(response, msgID))