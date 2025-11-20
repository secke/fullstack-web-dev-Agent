"""Configuration for the Full-Stack Multi-Agent System."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    OUTPUTS_DIR: Path = BASE_DIR / "outputs"
    TEMPLATES_DIR: Path = BASE_DIR / "src" / "templates"
    
    # HuggingFace
    HF_TOKEN: str = ""
    HF_MODEL: str = "meta-llama/Llama-3.1-8B-Instruct"
    
    # Agent Configuration
    MAX_STEPS: int = 15
    VERBOSE: bool = True
    
    # Code Generation
    DEFAULT_BACKEND_FRAMEWORK: str = "fastapi"
    DEFAULT_FRONTEND_FRAMEWORK: str = "react"
    DEFAULT_DB: str = "sqlite"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

settings = Settings()
