from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    environment: str
    database_url: str
    storage_path: str
    log_level: str
    
    # Claude AI Configuration
    claude_api_key: str = ""
    claude_model: str = "claude-sonnet-4-6"
    claude_timeout: int = 60
    claude_max_retries: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
