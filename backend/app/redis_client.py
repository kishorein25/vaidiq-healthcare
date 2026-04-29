"""
Redis Connection Module
Handles async Redis connections for caching and real-time queue management
Uses Upstash Redis for free-tier production deployment
"""

import redis.asyncio as redis
from app.config.settings import settings
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

# Global Redis client
redis_client: redis.Redis = None


async def connect_to_redis():
    """
    Create Redis connection on application startup
    Uses redis.asyncio for async operations
    """
    global redis_client
    
    try:
        logger.info("🔌 Connecting to Redis...")
        
        redis_client = await redis.from_url(
            settings.REDIS_URL,
            encoding="utf8",
            decode_responses=True,
            socket_connect_timeout=5,
            socket_keepalive=True
        )
        
        # Test connection
        await redis_client.ping()
        logger.info("✅ Connected to Redis successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to connect to Redis: {str(e)}")
        # Don't raise - allow app to work without Redis (graceful degradation)
        logger.warning("⚠️ Continuing without Redis - cache features will be unavailable")
        redis_client = None


async def close_redis_connection():
    """
    Close Redis connection on application shutdown
    """
    global redis_client
    
    try:
        if redis_client:
            await redis_client.close()
            logger.info("✅ Redis connection closed")
    except Exception as e:
        logger.error(f"❌ Error closing Redis connection: {str(e)}")


def get_redis() -> redis.Redis:
    """
    Get Redis client instance
    Use in dependency injection
    """
    if redis_client is None:
        logger.warning("⚠️ Redis not available - some features may be unavailable")
        return None
    return redis_client


# Queue Management Functions

async def get_next_queue_token() -> int:
    """
    Generate next queue token number (100x faster than DB)
    Increments counter in Redis
    
    Returns:
        Next token number
    """
    if not redis_client:
        logger.warning("Redis not available for queue token generation")
        return None
    
    try:
        token = await redis_client.incr("queue:token_counter")
        logger.info(f"📋 Generated queue token: {token}")
        return token
    except Exception as e:
        logger.error(f"❌ Error generating queue token: {str(e)}")
        return None


async def get_current_serving_token() -> int:
    """
    Get current serving token number from queue
    
    Returns:
        Current serving token
    """
    if not redis_client:
        return None
    
    try:
        token = await redis_client.get("queue:current_serving")
        return int(token) if token else 0
    except Exception as e:
        logger.error(f"❌ Error getting current serving token: {str(e)}")
        return None


async def set_current_serving_token(token: int):
    """
    Update current serving token in queue
    
    Args:
        token: Token number being served
    """
    if not redis_client:
        return
    
    try:
        await redis_client.set("queue:current_serving", token)
        logger.info(f"📋 Current serving token updated to: {token}")
    except Exception as e:
        logger.error(f"❌ Error setting serving token: {str(e)}")


async def get_queue_status() -> dict:
    """
    Get complete queue status
    
    Returns:
        Queue status information
    """
    if not redis_client:
        return {"status": "Redis unavailable"}
    
    try:
        current_serving = await get_current_serving_token()
        next_token = await redis_client.get("queue:token_counter")
        
        return {
            "current_serving": current_serving or 0,
            "next_token": int(next_token) if next_token else 0,
            "waiting_count": (int(next_token) if next_token else 0) - (current_serving or 0)
        }
    except Exception as e:
        logger.error(f"❌ Error getting queue status: {str(e)}")
        return {"status": "error"}


async def reset_queue():
    """
    Reset queue to start from token 0
    Use with caution - only for end of day/week
    """
    if not redis_client:
        return
    
    try:
        await redis_client.delete("queue:token_counter")
        await redis_client.delete("queue:current_serving")
        logger.info("🔄 Queue reset successfully")
    except Exception as e:
        logger.error(f"❌ Error resetting queue: {str(e)}")


# Caching Functions

async def set_cache(key: str, value: dict, expiration_hours: int = 24):
    """
    Set a value in cache with expiration
    
    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        expiration_hours: Expiration time in hours
    """
    if not redis_client:
        return
    
    try:
        json_value = json.dumps(value)
        await redis_client.setex(
            key,
            timedelta(hours=expiration_hours),
            json_value
        )
        logger.debug(f"💾 Cached key: {key} (expires in {expiration_hours}h)")
    except Exception as e:
        logger.error(f"❌ Error setting cache for {key}: {str(e)}")


async def get_cache(key: str) -> dict:
    """
    Get a value from cache
    
    Args:
        key: Cache key
        
    Returns:
        Cached value or None
    """
    if not redis_client:
        return None
    
    try:
        value = await redis_client.get(key)
        if value:
            logger.debug(f"✅ Cache hit for key: {key}")
            return json.loads(value)
        logger.debug(f"❌ Cache miss for key: {key}")
        return None
    except Exception as e:
        logger.error(f"❌ Error getting cache for {key}: {str(e)}")
        return None


async def cache_exists(key: str) -> bool:
    """
    Check if a cache key exists
    
    Args:
        key: Cache key
        
    Returns:
        True if exists, False otherwise
    """
    if not redis_client:
        return False
    
    try:
        exists = await redis_client.exists(key)
        return bool(exists)
    except Exception as e:
        logger.error(f"❌ Error checking cache existence for {key}: {str(e)}")
        return False


async def delete_cache(key: str):
    """
    Delete a cache key
    
    Args:
        key: Cache key to delete
    """
    if not redis_client:
        return
    
    try:
        await redis_client.delete(key)
        logger.debug(f"🗑️ Deleted cache key: {key}")
    except Exception as e:
        logger.error(f"❌ Error deleting cache for {key}: {str(e)}")


async def invalidate_cache_pattern(pattern: str):
    """
    Invalidate all cache keys matching a pattern
    
    Args:
        pattern: Pattern to match (e.g., "user:123:*")
    """
    if not redis_client:
        return
    
    try:
        keys = await redis_client.keys(pattern)
        if keys:
            await redis_client.delete(*keys)
            logger.info(f"🗑️ Invalidated {len(keys)} cache keys matching pattern: {pattern}")
    except Exception as e:
        logger.error(f"❌ Error invalidating cache pattern {pattern}: {str(e)}")


# Session Management

async def create_session(user_id: int, user_type: str, token: str, expiration_hours: int = 24):
    """
    Create user session in cache
    
    Args:
        user_id: User ID
        user_type: Type of user (admin, doctor, nurse, patient)
        token: JWT token
        expiration_hours: Session expiration time
    """
    if not redis_client:
        return
    
    try:
        session_key = f"session:{user_id}"
        session_data = {
            "user_id": user_id,
            "user_type": user_type,
            "token": token,
            "created_at": datetime.utcnow().isoformat()
        }
        
        await set_cache(session_key, session_data, expiration_hours)
        logger.info(f"👤 Session created for user {user_id} ({user_type})")
    except Exception as e:
        logger.error(f"❌ Error creating session for user {user_id}: {str(e)}")


async def get_session(user_id: int) -> dict:
    """
    Get user session data
    
    Args:
        user_id: User ID
        
    Returns:
        Session data or None
    """
    if not redis_client:
        return None
    
    try:
        session_key = f"session:{user_id}"
        return await get_cache(session_key)
    except Exception as e:
        logger.error(f"❌ Error getting session for user {user_id}: {str(e)}")
        return None


async def invalidate_session(user_id: int):
    """
    Invalidate user session (logout)
    
    Args:
        user_id: User ID
    """
    if not redis_client:
        return
    
    try:
        session_key = f"session:{user_id}"
        await delete_cache(session_key)
        logger.info(f"👤 Session invalidated for user {user_id}")
    except Exception as e:
        logger.error(f"❌ Error invalidating session for user {user_id}: {str(e)}")


# Rate Limiting

async def check_rate_limit(key: str, max_requests: int = 100, window_seconds: int = 60) -> bool:
    """
    Check if request is within rate limit
    
    Args:
        key: Rate limit key (e.g., "user:123:api")
        max_requests: Max requests allowed
        window_seconds: Time window in seconds
        
    Returns:
        True if within limit, False otherwise
    """
    if not redis_client:
        return True  # Allow if Redis not available
    
    try:
        current = await redis_client.incr(key)
        
        if current == 1:
            await redis_client.expire(key, window_seconds)
        
        return current <= max_requests
    except Exception as e:
        logger.error(f"❌ Error checking rate limit for {key}: {str(e)}")
        return True  # Allow on error


# Appointment Caching

async def cache_appointment_availability(doctor_id: int, available_slots: list):
    """
    Cache doctor appointment availability
    
    Args:
        doctor_id: Doctor ID
        available_slots: List of available time slots
    """
    if not redis_client:
        return
    
    try:
        cache_key = f"doctor:{doctor_id}:availability"
        await set_cache(cache_key, {"slots": available_slots}, expiration_hours=2)
        logger.debug(f"📅 Cached availability for doctor {doctor_id}")
    except Exception as e:
        logger.error(f"❌ Error caching appointment availability: {str(e)}")


async def get_appointment_availability(doctor_id: int) -> list:
    """
    Get cached appointment availability for a doctor
    
    Args:
        doctor_id: Doctor ID
        
    Returns:
        List of available slots or None
    """
    if not redis_client:
        return None
    
    try:
        cache_key = f"doctor:{doctor_id}:availability"
        data = await get_cache(cache_key)
        return data.get("slots") if data else None
    except Exception as e:
        logger.error(f"❌ Error getting appointment availability: {str(e)}")
        return None
