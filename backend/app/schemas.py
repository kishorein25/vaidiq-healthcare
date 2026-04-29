"""
Pydantic Schemas for Request/Response Validation
Ensures type safety and data validation
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ==================== Auth Schemas ====================

class LoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123"
            }
        }


class RegisterRequest(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=3, max_length=255)
    phone: str = Field(..., regex=r'^\+?91?[6-9]\d{9}$')  # Indian phone format
    role: str = Field(..., regex=r'^(patient|doctor|nurse|admin)$')

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "doctor@clinic.com",
                "password": "SecurePass123",
                "full_name": "Dr. Raj Kumar",
                "phone": "9876543210",
                "role": "doctor"
            }
        }


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }


class UserResponse(BaseModel):
    """User profile response"""
    id: int
    email: str
    full_name: str
    phone: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Doctor Schemas ====================

class DoctorRegisterRequest(BaseModel):
    """Doctor registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str
    phone: str
    specialization: str = Field(..., min_length=3, max_length=255)
    qualification: str
    experience_years: int = Field(..., ge=0, le=60)
    license_number: str
    consulting_fee: float = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "dr.smith@hospital.com",
                "password": "SecurePass123",
                "full_name": "Dr. Smith",
                "phone": "9876543210",
                "specialization": "Cardiology",
                "qualification": "MD, MRCP",
                "experience_years": 10,
                "license_number": "MED123456",
                "consulting_fee": 500.0
            }
        }


class DoctorResponse(BaseModel):
    """Doctor profile response"""
    id: int
    user_id: int
    full_name: str
    email: str
    specialization: str
    experience_years: int
    consulting_fee: float
    rating: float
    total_patients: int
    total_appointments: int
    is_available: bool

    class Config:
        from_attributes = True


class DoctorUpdateRequest(BaseModel):
    """Update doctor profile"""
    specialization: Optional[str] = None
    consulting_fee: Optional[float] = Field(None, gt=0)
    is_available: Optional[bool] = None
    available_from: Optional[datetime] = None
    available_to: Optional[datetime] = None


# ==================== Patient Schemas ====================

class PatientRegisterRequest(BaseModel):
    """Patient registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str
    phone: str
    date_of_birth: Optional[datetime] = None
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_contact_name: Optional[str] = None


class PatientResponse(BaseModel):
    """Patient profile response"""
    id: int
    user_id: int
    full_name: str
    email: str
    blood_group: Optional[str]
    allergies: Optional[str]
    total_appointments: int
    last_appointment: Optional[datetime]

    class Config:
        from_attributes = True


class PatientUpdateRequest(BaseModel):
    """Update patient profile"""
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_contact_name: Optional[str] = None


# ==================== Appointment Schemas ====================

class AppointmentCreateRequest(BaseModel):
    """Create appointment request"""
    doctor_id: int
    appointment_date: datetime = Field(..., description="Appointment date and time")
    reason: str = Field(..., min_length=5, max_length=500)
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "doctor_id": 1,
                "appointment_date": "2026-05-15T10:30:00",
                "reason": "Regular checkup",
                "notes": "Patient has diabetes"
            }
        }


class AppointmentResponse(BaseModel):
    """Appointment response"""
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    status: str
    reason: str
    queue_token: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class AppointmentUpdateRequest(BaseModel):
    """Update appointment"""
    status: Optional[str] = None
    notes: Optional[str] = None


# ==================== Queue Schemas ====================

class QueueStatusResponse(BaseModel):
    """Queue status response"""
    current_serving: int
    next_token: int
    waiting_count: int


class QueueEntryResponse(BaseModel):
    """Queue entry response"""
    id: int
    patient_id: int
    appointment_id: int
    token_number: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== AI Chat Schemas ====================

class ChatMessageRequest(BaseModel):
    """AI chat message request"""
    message: str = Field(..., min_length=1, max_length=1000)
    context: Optional[str] = None  # Medical context if any

    class Config:
        json_schema_extra = {
            "example": {
                "message": "What are the symptoms of diabetes?",
                "context": "Patient query"
            }
        }


class ChatMessageResponse(BaseModel):
    """AI chat response"""
    user_message: str
    ai_response: str
    confidence: float
    timestamp: datetime


# ==================== Error Schemas ====================

class ErrorResponse(BaseModel):
    """Standard error response"""
    status: str = "error"
    message: str
    detail: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "message": "Invalid credentials",
                "detail": {"field": "email", "issue": "not found"},
                "timestamp": "2026-04-29T12:00:00"
            }
        }


class SuccessResponse(BaseModel):
    """Standard success response"""
    status: str = "success"
    message: str
    data: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Operation completed",
                "data": {"id": 1, "name": "John"},
                "timestamp": "2026-04-29T12:00:00"
            }
        }
