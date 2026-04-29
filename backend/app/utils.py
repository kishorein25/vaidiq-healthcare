"""
Utility Functions
Common helpers used throughout the application
"""

import re
import logging
from datetime import datetime
from typing import Optional
import secrets

logger = logging.getLogger(__name__)


# ==================== Validation Functions ====================

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone_india(phone: str) -> bool:
    """
    Validate Indian phone number format
    
    Args:
        phone: Phone number
        
    Returns:
        True if valid Indian phone, False otherwise
    """
    pattern = r'^\+?91?[6-9]\d{9}$'
    return bool(re.match(pattern, phone.replace(" ", "").replace("-", "")))


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Must have: 8+ chars, uppercase, lowercase, digit, special char
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain digit"
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return False, "Password must contain special character"
    
    return True, "Password is strong"


def validate_blood_group(blood_group: str) -> bool:
    """
    Validate blood group format
    
    Args:
        blood_group: Blood group
        
    Returns:
        True if valid, False otherwise
    """
    valid_groups = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]
    return blood_group.upper() in valid_groups


# ==================== Token Generation ====================

def generate_queue_token() -> int:
    """
    Generate unique queue token number
    
    Returns:
        Random token number (1000-9999)
    """
    return secrets.randbelow(9000) + 1000


def generate_secure_token(length: int = 32) -> str:
    """
    Generate secure random token
    
    Args:
        length: Token length
        
    Returns:
        Secure random token
    """
    return secrets.token_urlsafe(length)


# ==================== DateTime Functions ====================

def get_ist_now() -> datetime:
    """
    Get current time in IST (Indian Standard Time)
    
    Returns:
        Current datetime in IST
    """
    from datetime import timezone, timedelta
    IST = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(IST)


def format_datetime(dt: datetime, format_str: str = "%d-%m-%Y %H:%M:%S") -> str:
    """
    Format datetime object to string
    
    Args:
        dt: Datetime object
        format_str: Format string
        
    Returns:
        Formatted datetime string
    """
    if dt is None:
        return ""
    return dt.strftime(format_str)


def time_until_appointment(appointment_datetime: datetime) -> dict:
    """
    Calculate time remaining until appointment
    
    Args:
        appointment_datetime: Appointment date/time
        
    Returns:
        Dict with days, hours, minutes remaining
    """
    now = get_ist_now()
    remaining = appointment_datetime - now
    
    days = remaining.days
    seconds = remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "total_minutes": int(remaining.total_seconds() / 60)
    }


# ==================== File Handling ====================

def get_file_extension(filename: str) -> str:
    """
    Get file extension
    
    Args:
        filename: Filename
        
    Returns:
        File extension (lowercase)
    """
    return filename.rsplit(".", 1)[1].lower() if "." in filename else ""


def is_allowed_file(filename: str, allowed_extensions: list) -> bool:
    """
    Check if file extension is allowed
    
    Args:
        filename: Filename
        allowed_extensions: List of allowed extensions
        
    Returns:
        True if allowed, False otherwise
    """
    ext = get_file_extension(filename)
    return ext in allowed_extensions


def generate_safe_filename(original_filename: str, user_id: int, prefix: str = "") -> str:
    """
    Generate safe filename with user ID and timestamp
    
    Args:
        original_filename: Original filename
        user_id: User ID
        prefix: Prefix for filename
        
    Returns:
        Safe filename
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    ext = get_file_extension(original_filename)
    filename = f"{prefix}_{user_id}_{timestamp}.{ext}" if prefix else f"{user_id}_{timestamp}.{ext}"
    return filename


# ==================== Response Formatters ====================

def format_success_response(data: dict, message: str = "Success") -> dict:
    """
    Format successful API response
    
    Args:
        data: Response data
        message: Success message
        
    Returns:
        Formatted response dict
    """
    return {
        "status": "success",
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }


def format_error_response(message: str, detail: Optional[dict] = None, status_code: int = 400) -> dict:
    """
    Format error API response
    
    Args:
        message: Error message
        detail: Additional error details
        status_code: HTTP status code
        
    Returns:
        Formatted error response dict
    """
    return {
        "status": "error",
        "message": message,
        "detail": detail or {},
        "status_code": status_code,
        "timestamp": datetime.utcnow().isoformat()
    }


# ==================== Health Check ====================

def format_health_check(db_status: str, redis_status: str, mongo_status: str) -> dict:
    """
    Format health check response
    
    Args:
        db_status: PostgreSQL status
        redis_status: Redis status
        mongo_status: MongoDB status
        
    Returns:
        Health check response
    """
    overall_status = "healthy" if all(s == "connected" for s in [db_status, redis_status, mongo_status]) else "degraded"
    
    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "postgresql": db_status,
            "redis": redis_status,
            "mongodb": mongo_status
        }
    }
