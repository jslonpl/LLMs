import os
from qdrant_client import QdrantClient as BaseQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http.models import UpdateStatus
from dotenv import load_dotenv
from typing import List, Dict, Optional, Union

class QdrantClient:
    def __init__(self):
        load_dotenv()
        self.url = self._get_full_url()
        self._api_key = self._get_env_var("QDRANT_API_KEY")
        self.client = self._initialize_client()
        
    def show_url(self):
        return self.url

    def _get_env_var(self, var_name: str, default: Optional[str] = None) -> str:
        """
        Handle loading environmental variable.

        Parameters:
            var_name (str): Name of environmental variable to loading
            dafault (Optional[str]) : Defalt value that will be returned if var_name is not set

        Returns:
            value (str) : Loaded environmental variable if set, otherwise None
        """
        value = os.getenv(var_name)
        if not value and default is None:
            raise ValueError(f"Environment variable {var_name} is not set.")
        return str(value) if value else default



    def _get_full_url(self) -> str:
        """
        Construct the full Qdrant URL from environment variables.

        Returns:
            str: The complete URL with host and port

        Raises:
            ValueError: If required environment variables are missing or invalid
        """
        base_url = self._get_env_var("QDRANT_URL")
        port = self._get_env_var("QDRANT_PORT")

        if base_url is None:
            raise ValueError("QDRANT_URL environment variavle is not set.")
        if port is None:
            raise ValueError("QDRANT_PORT environment variavle is not set.")
        
        return f"{base_url}:{port}"
    
    def _initialize_client(self) -> BaseQdrantClient:
        """ Initialized and returns instance of BaseQdrantClient """
        return BaseQdrantClient(
            url = self.url, 
            api_key=self._api_key
        )
    
    def list_collections(self) -> List[str]:
        """
        Get a list of all existing collections.

        Returns:
            List[str] : Names of all collections in the Qdrant instance

        Raises:
            Exceptions: If the operation fails
        """
        try:
            collections = self.client.get_collections()
            return [collection.name for collection in collections.collections]
        except Exception as e:
            raise Exception(f"Failed to list collections: {str(e)}")