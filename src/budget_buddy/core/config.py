# 📁 core/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_settings():
    """Get application settings from environment variables"""
    
    return {
        # OpenAI Configuration
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "gpt-4o"),
        
        # Application Configuration
        "APP_NAME": os.getenv("APP_NAME", "Budget Buddy"),
        "APP_VERSION": os.getenv("APP_VERSION", "1.0.0"),
        "APP_DESCRIPTION": os.getenv("APP_DESCRIPTION", "AI-powered finance assistant for tracking income and expenses"),
        
        # Environment
        "ENVIRONMENT": os.getenv("ENVIRONMENT", "development"),
        "DEBUG": os.getenv("DEBUG", "True").lower() == "true" or os.getenv("ENVIRONMENT", "development").lower() == "development",
        
        # Database Configuration
        "DATABASE_URL": os.getenv("DATABASE_URL", "sqlite:///./budget_buddy.db"),
    }

# Create settings instance
settings = get_settings()

def validate_settings():
    """Validate required configuration."""
    if not settings["OPENAI_API_KEY"]:
        raise ValueError("OPENAI_API_KEY is required. Please set it in your .env file.")

# Export settings
__all__ = ["settings", "validate_settings"] 