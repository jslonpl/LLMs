import os
import sys
from pathlib import Path
import logging

# Get the absolute path to the project root directory
project_root = Path(__file__).resolve().parents[2]

# Add the project root to sys.path
sys.path.append(str(project_root))

from src.api.neo4j.client import Neo4jClient
from src.utils.file_handler import FileHandler

def load_csv_to_neo4j_as_nodes():
    query = {
        "create_nodes": """
        UNWIND $data AS userData
        MERGE (u:User {id: userData.id})
        ON CREATE SET
            u.name = userData.username
        """
        }
    try:
        file_handler = FileHandler()
        neo4j_client = Neo4jClient()
        csv_path = "files/pliki_z_fabryki/rdb/users.csv"
        data = file_handler.load_csv(csv_path)

        neo4j_client.connect()
        #neo4j_client.delete_all_nodes()
        neo4j_client.execute_query(query["create_nodes"], parameters={"data": data})
        logging.info(f"Successfully loaded {len(data)} users into Neo4j")
    except Exception as e:
        logging.error(f"Failed to load CSV to Neo4j. Error type: {type(e).__name__}")
        logging.error(f"Error message: {str(e)}")
        raise
    finally:
        if "neo4j_client" in locals():
            neo4j_client.close()

def load_csv_to_neo4j_as_relations():
    
    query = {
        "create_relations": """
        UNWIND $rels AS rel
        MATCH (u1:User {id: rel.user1_id})
        MATCH (u2:User {id: rel.user2_id})
        MERGE (u1)-[:KNOWS]->(u2)
        """
        }
    
    try:
        file_handler = FileHandler()
        neo4j_client = Neo4jClient()
        csv_path = "files/pliki_z_fabryki/rdb/connections.csv"
        relations = file_handler.load_csv(csv_path)

        neo4j_client.connect()
        #neo4j_client.delete_all_nodes()
        neo4j_client.execute_query(query["create_relations"], parameters={"rels": relations})
        logging.info(f"Successfully loaded {len(relations)} users into Neo4j")
    except Exception as e:
        logging.error(f"Failed to load CSV to Neo4j. Error type: {type(e).__name__}")
        logging.error(f"Error message: {str(e)}")
        raise
    finally:
        if "neo4j_client" in locals():
            neo4j_client.close()

def test_connection():
    client = Neo4jClient()
    try:
        client.connect()
        print("Connection successful!")
        return True
    except Exception as e:
        print(f"Connection failed: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        return False
    finally:
        client.close()

def operations_on_graph():
    
    query = {
        "show_all_relations": "MATCH (n)-[r]->(m) RETURN n, r, m",
        "shortest_path":"""MATCH p=shortestPath((r:User {name: "Rafał"})-[*]-(b:User {name: "Barbara"})) RETURN p"""
        }
    
    try:
        neo4j_client = Neo4jClient()
        neo4j_client.connect()
        res = neo4j_client.execute_query(query["shortest_path"])
        logging.info(f"{res}")
    except Exception as e:
        logging.error(f"Failed to load CSV to Neo4j. Error type: {type(e).__name__}")
        logging.error(f"Error message: {str(e)}")
        raise
    finally:
        if "neo4j_client" in locals():
            neo4j_client.close()


operations_on_graph()