import sys
from loguru import logger
from app.config.settings import settings

def setup_logger():
    """
    Configures the centralized Loguru logger.
    Removes default handlers and adds custom ones based on settings.
    """
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
