import os
from dotenv import load_dotenv

class Config:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._load_env()
        return cls._instance
    
    @classmethod
    def _load_env(cls):
        # load environmental variable from .env file and savind them inro _config dictionary
        load_dotenv()
        cls._config = {key:value for key, value in os.environ.items()}

    @classmethod
    def get_key(cls, key_name, default=None):
        # return value for certain env key if exists. If key don't exist return default value=None
        if cls._config is None:
            cls._load_env()
        return cls._config.get(key_name, default)
    
    @classmethod
    def get_all_keys(cls):
        # return _config dictionary containing all keys from .env file
        return cls._config