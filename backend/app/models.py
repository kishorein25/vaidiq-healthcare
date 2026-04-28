from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

# USERS TABLE
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)  # admin, doctor, patient, nurse


# DOCTOR TABLE
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    gov_id_number = Column(String)
    certificate_path = Column(String)

    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)


# PATIENT TABLE
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))


# APPOINTMENT / QUEUE TABLE
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer)
    patient_id = Column(Integer)

    token_number = Column(Integer)
    status = Column(String, default="waiting")

    created_at = Column(DateTime, default=datetime.utcnow)