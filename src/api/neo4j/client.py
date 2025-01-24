from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Neo4jClient:
    def __init__(self):
        load_dotenv()
        self.uri = self._get_env_var("NEO4J_URI")
        self.user = self._get_env_var("NEO4J_USER")
        self.password = self._get_env_var("NEO4J_PASSWORD")
        self.driver = None

    def _get_env_var(self, var_name: str) -> str:
        value = os.getenv(var_name)
        if not value:
            raise ValueError(f"Environment variable {var_name} is not set.")
        return value
    
    def connect(self):
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            logging.info(f"Successfully connected to Neo4j database.")
        except Exception as e:
            logging.error(f"Failed to connect to Neo4j: {str(e)}")
            raise

    def close(self):
        if self.driver:
            self.driver.close()
            logging.info(f"Neo4j connection closed.")

    def execute_query(self, query: str, parameters: dict = None) -> list:
        """
        Execute a Cypher query against Neo4j database and return results.

        Parameters:
            query (str) : The Cypher query to execute.
                Example: "MATCH (n:Person) WHERE n.age > $min_age RETURN n"
            parameters (dict, optional): Dictionary of query parameters
                Example: {"min_age": 25}
        
        Returns:
            list: List of dictionaries containing query results.
                Example: [
                    {"n": {"name": "John", "age": 30}},
                    {"n": {"name": "Alice", "age": 28}}
                ]
        """
        if not self.driver:
            raise RuntimeError("Not connected to Neo4j. Call connect() first.")
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            logging.error(f"Query execution failed: {str(e)}")
            raise


    def delete_all_nodes(self) -> None:
        " Method delete all nodes from Graph DataBase"
        try:
            self.execute_query("MATCH (n) DETACH DELETE n")
            logging.info(f"All nodes has been deleted.")
        except Exception as e:
            logging.error(f"Deleting nodes failed: {str(e)}")
            raise