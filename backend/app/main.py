from fastapi import FastAPI, Request
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
from app.api.debug import router as debug_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    log.info(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    # Shutdown logic
    log.info(f"Shutting down {settings.app_name}")

def create_app() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_cors_origins,
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
    app.include_router(debug_router, prefix="/api")
    app.include_router(chat_router, prefix="/api")
    app.include_router(research_router, prefix="/api")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
# trigger reload
