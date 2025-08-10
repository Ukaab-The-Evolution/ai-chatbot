"""
FastAPI application factory.
Following Single Responsibility Principle - handles only app creation and configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .api.routes import chat, utils
from .utils.logging import setup_logging


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI app instance
    """
    # Setup logging
    setup_logging("INFO" if not settings.debug else "DEBUG")
    
    # Create FastAPI app
    app = FastAPI(
        title="Truck Driver Assistant API",
        description="AI-powered chatbot API for Pakistani truck drivers with multi-language support",
        version="1.0.0",
        docs_url="/docs",
        debug=settings.debug
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(chat.router)
    app.include_router(utils.router)
    
    return app


# Create app instance
app = create_app()
