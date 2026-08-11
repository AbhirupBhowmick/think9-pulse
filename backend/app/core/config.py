import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union
from pydantic import field_validator

# Compute absolute path to default SQLite database in project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
default_db_path = os.path.join(project_root, "think9_pulse.db")
backend_seed_db_path = os.path.join(backend_dir, "think9_pulse.db")

# Detect Vercel serverless environment or read-only filesystem
is_vercel = os.getenv("VERCEL") == "1" or os.getenv("VERCEL_ENV") is not None or not os.access(project_root, os.W_OK)

if is_vercel:
    tmp_db_path = "/tmp/think9_pulse.db"
    # Locate bundled seed database (check project root first, then backend dir)
    seed_db = default_db_path if os.path.exists(default_db_path) else (backend_seed_db_path if os.path.exists(backend_seed_db_path) else None)
    if seed_db and not os.path.exists(tmp_db_path):
        import shutil
        shutil.copy2(seed_db, tmp_db_path)
    runtime_db_path = tmp_db_path if os.path.exists(tmp_db_path) else default_db_path
else:
    runtime_db_path = default_db_path

# Explicitly load .env from backend/.env or root .env
backend_env_path = os.path.join(backend_dir, ".env")
root_env_path = os.path.join(project_root, ".env")

if os.path.exists(backend_env_path):
    load_dotenv(dotenv_path=backend_env_path, override=True)
elif os.path.exists(root_env_path):
    load_dotenv(dotenv_path=root_env_path, override=True)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Think9 Pulse API"
    API_V1_STR: str = "/api/v1"
    APP_ENV: str = "development"
    
    # Database
    DATABASE_URL: str = f"sqlite:///{runtime_db_path}"
    
    # AI Service Configuration
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_NAME: str = "gemini-3.6-flash"
    DEMO_MODE: bool = False
    
    # CORS
    CORS_ORIGINS: Union[str, List[str]] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
