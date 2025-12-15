from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"
    neo4j_client_id: str | None = None
    neo4j_client_secret: str | None = None
    low_conf_threshold: float = 0.6
    llm_api_key: str | None = None
    llm_model: str = "gemini-2.0-flash"
    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()


