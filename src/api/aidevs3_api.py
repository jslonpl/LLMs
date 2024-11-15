import requests
import json
import os
from dotenv import load_dotenv

class PoligonAiDevs3API():
    def __init__(self, apikey, task_url, endpoint_url):
        self.apikey = self.get_apikey()
        self.task_url = task_url
        self.endpoint_url = endpoint_url

    def get_apikey(self):
        load_dotenv()
        ai_devs_3_api_key = os.getenv('AI_DEVS_3_API_KEY')
        return ai_devs_3_api_key

        