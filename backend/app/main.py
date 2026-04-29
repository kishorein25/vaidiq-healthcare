"""
VaidiQ Healthcare - Main FastAPI Application
AI-Powered Smart Healthcare Clinic Management System
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from app.config.settings import settings
from app.database import init_db, close_db, get_db
from app.mongodb import connect_to_mongo, close_mongo_connection
from app.redis_client import connect_to_redis, close_redis_connection
from app.utils import format_health_check

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==================== Lifespan Events ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown events
    Initialize all connections on startup
    Close all connections on shutdown
    """
    # ===== STARTUP =====
    logger.info("🚀 Starting VaidiQ Healthcare Application...")
    
    try:
        # Initialize PostgreSQL
        await init_db()
        logger.info("✅ PostgreSQL initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize PostgreSQL: {e}")
        raise
    
    try:
        # Initialize MongoDB
        await connect_to_mongo()
        logger.info("✅ MongoDB initialized")
    except Exception as e:
        logger.error(f"⚠️ MongoDB initialization warning: {e}")
        # Continue without MongoDB for graceful degradation
    
    try:
        # Initialize Redis
        await connect_to_redis()
        logger.info("✅ Redis initialized")
    except Exception as e:
        logger.error(f"⚠️ Redis initialization warning: {e}")
        # Continue without Redis for graceful degradation
    
    logger.info("✨ All services initialized successfully")
    logger.info(f"🌐 Server running at {settings.ENVIRONMENT} mode")
    
    yield
    
    # ===== SHUTDOWN =====
    logger.info("🛑 Shutting down VaidiQ Healthcare Application...")
    
    try:
        await close_db()
        logger.info("✅ PostgreSQL closed")
    except Exception as e:
        logger.error(f"Error closing PostgreSQL: {e}")
    
    try:
        await close_mongo_connection()
        logger.info("✅ MongoDB closed")
    except Exception as e:
        logger.error(f"Error closing MongoDB: {e}")
    
    try:
        await close_redis_connection()
        logger.info("✅ Redis closed")
    except Exception as e:
        logger.error(f"Error closing Redis: {e}")
    
    logger.info("✨ All services shut down successfully")


# ==================== Create FastAPI App ====================

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Smart Healthcare Clinic Management System",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)


# ==================== Middleware ====================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Error Handlers ====================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for all unhandled errors
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=exc)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ==================== Routes ====================

# Health Check Routes
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Simple health check endpoint
    """
    return {
        "status": "ok",
        "message": "VaidiQ Healthcare is running",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health/detailed", tags=["Health"])
async def detailed_health_check():
    """
    Detailed health check with all services status
    """
    from app.database import engine
    from app.mongodb import mongodb_client
    from app.redis_client import redis_client
    
    db_status = "connected"
    mongo_status = "connected" if mongodb_client else "disconnected"
    redis_status = "connected" if redis_client else "disconnected"
    
    # Test PostgreSQL
    try:
        if engine:
            async with engine.begin() as conn:
                await conn.exec_driver_sql("SELECT 1")
    except Exception as e:
        logger.warning(f"PostgreSQL health check failed: {e}")
        db_status = "error"
    
    # Test MongoDB
    try:
        if mongodb_client:
            await mongodb_client.admin.command('ping')
    except Exception as e:
        logger.warning(f"MongoDB health check failed: {e}")
        mongo_status = "error"
    
    # Test Redis
    try:
        if redis_client:
            await redis_client.ping()
    except Exception as e:
        logger.warning(f"Redis health check failed: {e}")
        redis_status = "error"
    
    return format_health_check(db_status, redis_status, mongo_status)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "AI-Powered Smart Healthcare Clinic Management System",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "redoc": "/redoc",
        "timestamp": datetime.utcnow().isoformat()
    }


# ==================== Routes Placeholder ====================
# These will be imported from respective route modules

# TODO: Import and include routers
# from app.routes import admin, doctor, nurse, patient, appointment, queue, ai_chat
# app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
# app.include_router(doctor.router, prefix="/api/doctor", tags=["Doctor"])
# app.include_router(nurse.router, prefix="/api/nurse", tags=["Nurse"])
# app.include_router(patient.router, prefix="/api/patient", tags=["Patient"])
# app.include_router(appointment.router, prefix="/api/appointment", tags=["Appointment"])
# app.include_router(queue.router, prefix="/api/queue", tags=["Queue"])
# app.include_router(ai_chat.router, prefix="/api/ai", tags=["AI Chat"])


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
