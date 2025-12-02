from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Neo4j connection - for local or Aura
    neo4j_uri: str = "bolt://localhost:7687"  # For Aura: neo4j+s://xxxxx.databases.neo4j.io
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"
    
    # Neo4j OAuth credentials (for Aura OAuth authentication)
    neo4j_client_id: str | None = None
    neo4j_client_secret: str | None = None
    
    low_conf_threshold: float = 0.6

    llm_api_key: str | None = None
    llm_model: str = "gemini-1.5-flash"  # or "gemini-pro" for more capable model

    model_config = {"env_file": ".env", "extra": "ignore"}  # Ignore extra env vars like GOOGLE_API_KEY


settings = Settings()


