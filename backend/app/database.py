"""
PostgreSQL Database Connection Module
Handles async SQLAlchemy connections for relational data
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool, QueuePool
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Base class for all ORM models
Base = declarative_base()

# Global database engine
engine = None
AsyncSessionLocal = None


async def init_db():
    """
    Initialize database engine and session factory on startup
    """
    global engine, AsyncSessionLocal
    
    try:
        logger.info("🔌 Initializing PostgreSQL connection...")
        
        # Create async engine
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DB_ECHO,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_recycle=settings.DB_POOL_RECYCLE,
            poolclass=QueuePool if settings.ENVIRONMENT == "production" else NullPool,
            connect_args={
                "server_settings": {"jit": "off"},
                "timeout": 30,
            }
        )
        
        # Create session factory
        AsyncSessionLocal = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )
        
        # Test connection
        async with engine.begin() as conn:
            await conn.exec_driver_sql("SELECT 1")
        
        logger.info("✅ PostgreSQL connected successfully")
        
        # Create all tables
        await create_tables()
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {str(e)}")
        raise e


async def create_tables():
    """
    Create all database tables from models
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database tables created/verified")
    except Exception as e:
        logger.error(f"❌ Error creating tables: {str(e)}")
        raise e


async def close_db():
    """
    Close database connection on shutdown
    """
    try:
        if engine:
            await engine.dispose()
            logger.info("✅ PostgreSQL connection closed")
    except Exception as e:
        logger.error(f"❌ Error closing database: {str(e)}")


async def get_db() -> AsyncSession:
    """
    Dependency to get database session
    Use in route handlers: async def route(db: AsyncSession = Depends(get_db))
    """
    if AsyncSessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            await session.close()
