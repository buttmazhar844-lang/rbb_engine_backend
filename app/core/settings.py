from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    environment: str
    database_url: str
    storage_path: str
    log_level: str
    
    # Claude AI Configuration
    claude_api_key: str = ""
    claude_model: str = "claude-3-5-sonnet-20241022"
    claude_timeout: int = 60
    claude_max_retries: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
