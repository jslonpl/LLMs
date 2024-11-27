import os
from dotenv import load_dotenv


class Aidevs3Client:
    def __init__(self):
        load_dotenv()
        self._api_key = self._get_env_var('AI_DEVS_3_API_KEY')
        self._endpoint_url = self._get_env_var('AI_DEVS_3_ENDPOINT_URL')
        self._data_url = self._get_env_var('AI_DEVS_3_DATA_URL')
        self._dane_url = self._get_env_var('AI_DEVS_3_DANE_URL')

    def _get_env_var(self, var_name: str) -> str:
        value = os.getenv(var_name)
        if not value:
            raise ValueError(f"Environment variable {var_name} is not set.")
        return value

    def get_api_key(self):
        return self._api_key

    def get_endpoint_url(self):
        return self._endpoint_url
    
    def get_data_url(self):
        return self._data_url
    
    def get_dane_url(self):
        return self._dane_url