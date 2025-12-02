from neo4j import GraphDatabase, Driver
import httpx
import ssl
import certifi

from ..config import settings

_driver: Driver | None = None


def _create_ssl_context() -> ssl.SSLContext:
    """
    Create SSL context for Neo4j Aura connections using certifi certificates.
    """
    context = ssl.create_default_context(cafile=certifi.where())
    return context


def _get_oauth_token() -> str | None:
    """
    Exchange OAuth credentials for an access token.
    This is used for Neo4j Aura with OAuth authentication.
    """
    if not settings.neo4j_client_id or not settings.neo4j_client_secret:
        return None
    
    try:
        # Neo4j Aura OAuth token endpoint
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
        # If OAuth fails, fall back to username/password
        return None


def get_driver() -> Driver:
    global _driver
    if _driver is None:
        # Try OAuth bearer token first if credentials are provided
        oauth_token = _get_oauth_token()
        
        # For Neo4j Aura (neo4j+s://), SSL is handled automatically by the URI scheme
        # The driver will use system certificates or certifi certificates
        # We don't need to pass ssl_context when using +s:// scheme
        
        if oauth_token:
            # Use bearer token authentication
            _driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=("", oauth_token),  # Neo4j driver uses empty user with token as password
            )
        else:
            # Fall back to username/password authentication
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


