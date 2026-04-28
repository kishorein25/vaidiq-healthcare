from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Doctor
from datetime import datetime

router = APIRouter(prefix="/admin")

@router.put("/verify/{doctor_id}")
def verify_doctor(doctor_id: int):
    db = SessionLocal()

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        return {"error": "Doctor not found"}

    doctor.is_verified = True
    doctor.verified_at = datetime.utcnow()

    db.commit()

    return {"msg": "Doctor verified"}