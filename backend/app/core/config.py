from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    app_name: str = "MESTA API"
    database_url: str = f"sqlite:///{BACKEND_DIR / 'mesta.db'}"
    max_upload_mb: int = 8
    top_k_matches: int = 5
    ai_api_key: str | None = None
    ai_model: str = ""
    demo_mode: bool = True
    frontend_origin: str = "http://localhost:3000"
    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")

settings = Settings()
