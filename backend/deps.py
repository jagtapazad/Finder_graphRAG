from neo4j import Driver

from .kg.client import get_driver


def get_neo4j_driver() -> Driver:
    """FastAPI dependency for accessing the shared Neo4j driver."""
    return get_driver()


