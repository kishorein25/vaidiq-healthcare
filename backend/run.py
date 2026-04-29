#!/usr/bin/env python
"""
Server runner script
Start the FastAPI server with this script

Usage:
    python run.py                    # Start with default settings
    python run.py --host 0.0.0.0    # Custom host
    python run.py --port 9000       # Custom port
    python run.py --reload           # Auto-reload on code changes
"""

import uvicorn
import sys
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)


def main():
    """
    Main entry point for server
    """
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         VaidiQ Healthcare - Starting Server               ║
    ║    AI-Powered Smart Healthcare Clinic Management System   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print(f"📍 Environment: {settings.ENVIRONMENT}")
    print(f"🚀 Server: {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    print(f"♻️ Reload: {settings.RELOAD}")
    print(f"📚 Docs: http://localhost:{settings.SERVER_PORT}/docs")
    print(f"📖 ReDoc: http://localhost:{settings.SERVER_PORT}/redoc")
    print()
    
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()
