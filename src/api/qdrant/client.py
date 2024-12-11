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
        
    
    def create_collections(self, collection_name: str, vector_size: int, distance: Distance = Distance.COSINE) -> bool:
        """
        Create new collection in Qdrant with given name.  
        
        Parameters:
            collection_name (str) : Name of creating collection
            vector_size (int) : Size of vector dimensions depending of embedding model - e.g. OpenAI embedding model vector size is 1536
            distance (Distance) : The way to compare similarity of vectors - for text the best is COSINE

        Returns:
            bool : True if collection is successfully created
        """
        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance)
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to create collectoin: {str(e)}")
        
    
    def collection_exists(self, collection_name: str) -> bool:
        """
        Check if collection exists in Qdrant.

        Parameters:
            collection_name (str) : Name of the collection to check

        Returns:
            bool: True if collection exists, False otherwise
        """

    
    def get_collection(self, collection_name: str) -> Dict:
        """
        Get detailed information about a specific collection.

        Parameters:
            collection_name (str): Name of the collection to retrieve information about

        Returns:
            Dict: Collection information incliding vector configuration, points count, etc.

        Raises:
            Exception: If the operation fails or collection doesn't exist
        """
        try:
            collection_info = self.client.get_collection(collection_name=collection_name)
            return {
                "vectors_count": collection_info.vectors_count, 
                "points_count": collection_info.points_count, 
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "status": collection_info.status
            }
        except Exception as e:
            raise Exception(f"Failed to get collection info: {str(e)}")
    
    
    def upsert_points(self, collection_name: str, points: List[PointStruct]) -> UpdateStatus:
        """
        Insert or update points in the collection.

        Parameters:
            collection_name (str) : Name of collection
            points (List[PointStruct]) : Points containing id, vector and payload

        Returns:
            Update Status - Result of update

        Example:
        # Text Vectors (embeddings) and payloads
        points = [
        PointStruct(
            id="text_1",
            vector=[0.1, 0.2, 0.3, 0.4],  # Przykładowy embedding tekstu
            payload={"text": "Machine learning is awesome.", "category": "AI"}
            ),
        PointStruct(
            id="text_2",
            vector=[0.2, 0.3, 0.4, 0.5],
            payload={"text": "Deep learning is a subset of machine learning.", "category": "AI"}
            )
        ]
        """
        try:
            return self.client.upsert(
                collection_name = collection_name,
                points = points
            )
        except Exception as e:
            raise Exception(f"Failed to upsert points: {str(e)}")
        
    
    def search_points(
            self,
            collection_name: str, 
            query_vector: List[float],
            limit: int = 5,
            score_threshold: Optional[float] = None
    ) -> List[Dict]:
        """
        Search for nearesr vectors in the collection.

        Parameters:
            collection_name (str) : Name of collection
            query_vector (List[float]) : Embedding representation of Query
            limit (int) : Limit of returned points
            score_threshold (Optional[float]) : Similarity threshold above which results are returned
        """
        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold
            )
            return [
                {
                    "id": point.id,
                    "score": point.score,
                    "payload": point.payload
                } for point in results
            ]
        except Exception as e:
            raise Exception(f"Search failed: {str(e)}")
        
    
    def delete_points(self, collection_name: str, points_ids: List[Union[str, int]]) -> UpdateStatus:
        """
        Delete points from the collection for given ids.
        Parameters:
            collection_name (str) : Name of collection from which points will be deleted
            points_ids (List[str or int]) : List coniatinig ids of points to delete. Type str or int means that isdeas could be string or int, depending of the used notation

        Returns:
            Update Status - Result of update
        """
        try:
            return self.client.delete(
                collection_name=collection_name,
                points_selector=points_ids
            )
        except Exception as e:
            raise Exception(f"Failed to delete points: {str(e)}")
        

    def delete_collection(self, collection_name: str) -> bool:
        """
        Delete the collection. 
        
        Parameters:
            collection_name (str) : Name of colleciton to delete

        Returns:
            bool : True if deleted successfully
        """
        try:
            self.client.delete_collection(collection_name=collection_name)
            return True
        except Exception as e:
            raise Exception(f"Failsed to delete collection: {str(e)}")