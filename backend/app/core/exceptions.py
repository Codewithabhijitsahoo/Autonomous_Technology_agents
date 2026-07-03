from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from app.utils.logger import log
from app.exceptions.base_exception import BaseAppException
from app.utils.response import error_response

def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(BaseAppException)
    async def custom_app_exception_handler(request: Request, exc: BaseAppException):
        log.error(f"App exception on {request.method} {request.url}: {exc.message}")
        content = error_response(
            type=exc.type,
            message=exc.message,
            agent=exc.agent,
            node=exc.node,
            retryable=exc.retryable
        )
        return JSONResponse(status_code=400, content=content)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        log.error(f"Unhandled exception on {request.method} {request.url}: {exc}", exc_info=True)
        content = error_response(
            type="UnexpectedException",
            message="An unexpected system error occurred.",
            retryable=False
        )
        return JSONResponse(status_code=500, content=content)
