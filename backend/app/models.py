"""
SQLAlchemy ORM Models
Defines all database tables for VaidiQ Healthcare
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    """User role types"""
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    PATIENT = "patient"


class AppointmentStatus(str, enum.Enum):
    """Appointment status types"""
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class QueueStatus(str, enum.Enum):
    """Queue entry status"""
    WAITING = "waiting"
    CALLED = "called"
    SERVED = "served"
    NO_SHOW = "no_show"


class User(Base):
    """Base User model with role-based access"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.PATIENT, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    profile_image = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    admin_profile = relationship("Admin", back_populates="user", uselist=False, cascade="all, delete-orphan")
    doctor_profile = relationship("Doctor", back_populates="user", uselist=False, cascade="all, delete-orphan")
    nurse_profile = relationship("Nurse", back_populates="user", uselist=False, cascade="all, delete-orphan")
    patient_profile = relationship("Patient", back_populates="user", uselist=False, cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="patient")
    queue_entries = relationship("QueueEntry", back_populates="patient")


class Admin(Base):
    """Admin profile for clinic management"""
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    clinic_name = Column(String(255), nullable=False)
    clinic_address = Column(Text)
    clinic_phone = Column(String(20))
    license_number = Column(String(100))
    is_verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="admin_profile")


class Doctor(Base):
    """Doctor profile with specializations"""
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    specialization = Column(String(255), nullable=False)
    qualification = Column(Text)
    experience_years = Column(Integer, default=0)
    license_number = Column(String(100))
    license_document = Column(String(500))  # Path to uploaded file
    
    consulting_fee = Column(Float, default=500.0)
    available_from = Column(DateTime)
    available_to = Column(DateTime)
    is_available = Column(Boolean, default=True)
    rating = Column(Float, default=0.0)
    total_patients = Column(Integer, default=0)
    total_appointments = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="doctor_profile")
    appointments = relationship("Appointment", foreign_keys="Appointment.doctor_id", back_populates="doctor")


class Nurse(Base):
    """Nurse profile with shift management"""
    __tablename__ = "nurses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    license_number = Column(String(100))
    shift_start = Column(DateTime)
    shift_end = Column(DateTime)
    is_on_duty = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="nurse_profile")


class Patient(Base):
    """Patient profile with medical information"""
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    date_of_birth = Column(DateTime)
    blood_group = Column(String(10))
    allergies = Column(Text)
    emergency_contact = Column(String(20))
    emergency_contact_name = Column(String(255))
    
    total_appointments = Column(Integer, default=0)
    last_appointment = Column(DateTime)
    medical_history_mongodb_id = Column(String(500))  # Reference to MongoDB document
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="patient_profile")


class Appointment(Base):
    """Appointment booking system"""
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    appointment_date = Column(DateTime, nullable=False, index=True)
    appointment_time = Column(String(10), nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED)
    
    reason = Column(Text)
    notes = Column(Text)
    prescription_mongodb_id = Column(String(500))  # Reference to MongoDB
    
    queue_token = Column(Integer)
    token_generated_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship("User", foreign_keys=[patient_id], back_populates="appointments")
    doctor = relationship("Doctor", foreign_keys="Appointment.doctor_id", back_populates="appointments")


class QueueEntry(Base):
    """Real-time queue management"""
    __tablename__ = "queue_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    token_number = Column(Integer, nullable=False, index=True)
    status = Column(Enum(QueueStatus), default=QueueStatus.WAITING)
    
    called_at = Column(DateTime)
    served_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship("User", foreign_keys=[patient_id], back_populates="queue_entries")
