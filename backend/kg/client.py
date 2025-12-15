from neo4j import GraphDatabase, Driver
import httpx
import ssl
import certifi

from ..config import settings

_driver: Driver | None = None


def _create_ssl_context() -> ssl.SSLContext:
    context = ssl.create_default_context(cafile=certifi.where())
    return context


def _get_oauth_token() -> str | None:
    if not settings.neo4j_client_id or not settings.neo4j_client_secret:
        return None
    
    try:
        token_url = "https://api.neo4j.io/oauth/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": settings.neo4j_client_id,
            "client_secret": settings.neo4j_client_secret,
        }
        response = httpx.post(token_url, data=data, timeout=10.0)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("access_token")
    except Exception:
        return None


def get_driver() -> Driver:
    global _driver
    if _driver is None:
        oauth_token = _get_oauth_token()
        
        if oauth_token:
            _driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=("", oauth_token),
            )
        else:
            _driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password),
            )
    return _driver


def close_driver() -> None:
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


