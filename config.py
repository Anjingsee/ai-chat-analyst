from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url_mysql: str = "mysql+mysql-connector-python://root:password@localhost:3306/chat_db"
    database_url_pg: str = "postgresql://postgres:password@localhost:5432/chat_db"
    db_type: str = "postgres"  # mysql or postgres
    
    # LLM
    openai_api_key: Optional[str] = None
    llm_model: str = "gpt-4-turbo-preview"
    llm_provider: str = "openai"  # openai, claude, etc.
    
    # Server
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    debug: bool = True
    
    # File Upload
    max_file_size: int = 52428800  # 50MB
    upload_dir: str = "./uploads"
    allowed_file_types: str = "csv,xlsx,json,txt,pdf"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
