import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Enabled Skill Intelligence & Personalized Learning Platform"
    TARGET_ECOSYSTEM: str = "MoSPI / NSSTA / iGOT Karmayogi"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./skill_intelligence.db")
    
    # Anthropic API Key
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Demo Mode
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true" or not os.getenv("ANTHROPIC_API_KEY")
    
    # Mock iGOT
    MOCK_IGOT_BASE_URL: str = os.getenv("MOCK_IGOT_BASE_URL", "http://localhost:8000/mock-igot")
    
    # Rule Engine Version
    RULE_ENGINE_VERSION: str = "1.2.0"
    
    class Config:
        case_sensitive = True

settings = Settings()
