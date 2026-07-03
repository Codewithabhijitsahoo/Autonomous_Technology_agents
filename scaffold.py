import os
from pathlib import Path

BASE_DIR = Path("backend")
APP_DIR = BASE_DIR / "app"

folders = [
    "api",
    "agents",
    "graph",
    "services",
    "tools",
    "prompts",
    "models",
    "schemas",
    "config",
    "middleware",
    "utils",
    "constants",
    "core"
]

files = {
    BASE_DIR / ".env": """# Application Settings
APP_NAME=Deep Research Agent
APP_VERSION=1.0.0
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# Frontend URL for CORS
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000", "*"]
""",
    BASE_DIR / "requirements.txt": """fastapi
uvicorn
pydantic>=2.0.0
pydantic-settings>=2.0.0
loguru
python-dotenv
""",
    BASE_DIR / "README.md": """# Deep Research Agent Backend

This is the backend architecture for a production-grade Deep Research Agent.

## Architecture

The project follows a modular, scalable architecture with clear separation of concerns:

- `app/api/`: FastAPI route handlers (endpoints)
- `app/agents/`: LLM agents (e.g., Planner, Search, Validator)
- `app/graph/`: LangGraph workflow definitions
- `app/services/`: Core business logic and orchestration
- `app/tools/`: Custom tools for agents (e.g., search, scraper, PDF reader)
- `app/prompts/`: LLM system prompts and templates
- `app/models/`: Database models (if added in the future)
- `app/schemas/`: Pydantic models for data validation
- `app/config/`: Configuration management using Pydantic Settings
- `app/middleware/`: FastAPI middleware (e.g., rate limiting, auth)
- `app/utils/`: Shared utilities (e.g., logger)
- `app/constants/`: System-wide constants
- `app/core/`: Core system functionality (e.g., exception handling)

## Setup

1. Activate your virtual environment
2. Install requirements: `pip install -r requirements.txt`
3. Run the server: `uvicorn app.main:app --reload`
""",
    APP_DIR / "config" / "settings.py": """from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    \"\"\"
    Application settings, loaded from environment variables and .env file.
    \"\"\"
    app_name: str = "Deep Research Agent"
    app_version: str = "1.0.0"
    environment: str = "development"
    
    host: str = "0.0.0.0"
    port: int = 8000
    
    log_level: str = "INFO"
    
    cors_origins: List[str] = ["*"]
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
""",
    APP_DIR / "utils" / "logger.py": """import sys
from loguru import logger
from app.config.settings import settings

def setup_logger():
    \"\"\"
    Configures the centralized Loguru logger.
    Removes default handlers and adds custom ones based on settings.
    \"\"\"
    logger.remove()
    
    # Add stdout handler
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level.upper(),
    )
    
    # Add file handler for production or detailed logging
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="10 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
    )
    
    return logger

log = setup_logger()
""",
    APP_DIR / "core" / "exceptions.py": """from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from app.utils.logger import log

def add_exception_handlers(app: FastAPI) -> None:
    \"\"\"
    Registers global exception handlers for the FastAPI application.
    \"\"\"
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        log.error(f"Unhandled exception on {request.method} {request.url}: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )
""",
    APP_DIR / "api" / "health.py": """from fastapi import APIRouter
from app.config.settings import settings

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def health_check():
    \"\"\"
    Health check endpoint to verify system status.
    \"\"\"
    return {
        "status": "healthy",
        "version": settings.app_version
    }
""",
    APP_DIR / "api" / "chat.py": """from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("")
async def chat_endpoint():
    \"\"\"
    Placeholder endpoint for chat interaction.
    \"\"\"
    return {"message": "Chat endpoint not implemented yet."}
""",
    APP_DIR / "api" / "research.py": """from fastapi import APIRouter

router = APIRouter(prefix="/research", tags=["research"])

@router.post("")
async def start_research():
    \"\"\"
    Placeholder endpoint for triggering the Deep Research workflow.
    \"\"\"
    return {"message": "Research endpoint not implemented yet."}
""",
    APP_DIR / "main.py": """from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time

from app.config.settings import settings
from app.utils.logger import log
from app.core.exceptions import add_exception_handlers

# Import API Routers
from app.api.health import router as health_router
from app.api.chat import router as chat_router
from app.api.research import router as research_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    log.info(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    # Shutdown logic
    log.info(f"Shutting down {settings.app_name}")

def create_app() -> FastAPI:
    \"\"\"
    Factory function to create and configure the FastAPI application.
    \"\"\"
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request Logging Middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        log.info(f"Incoming request: {request.method} {request.url.path}")
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            log.info(f"Request completed: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
            return response
        except Exception as e:
            process_time = time.time() - start_time
            log.error(f"Request failed: {request.method} {request.url.path} - Time: {process_time:.4f}s")
            raise e

    # Register Global Exception Handlers
    add_exception_handlers(app)

    # Register API Routers
    app.include_router(health_router, prefix="/api")
    app.include_router(chat_router, prefix="/api")
    app.include_router(research_router, prefix="/api")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
"""
}

# Create directories and __init__.py files
for folder in folders:
    path = APP_DIR / folder
    path.mkdir(parents=True, exist_ok=True)
    (path / "__init__.py").touch()

# Ensure logs directory exists for the logger
(BASE_DIR / "logs").mkdir(parents=True, exist_ok=True)

# Write all files
for file_path, content in files.items():
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Backend scaffold created successfully.")
