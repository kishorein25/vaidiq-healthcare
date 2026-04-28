from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Appointment

router = APIRouter(prefix="/queue")

@router.post("/book")
def book_appointment(doctor_id: int, patient_id: int):
    db = SessionLocal()

    last = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id
    ).order_by(Appointment.token_number.desc()).first()

    token = 1 if not last else last.token_number + 1

    new_appointment = Appointment(
        doctor_id=doctor_id,
        patient_id=patient_id,
        token_number=token
    )

    db.add(new_appointment)
    db.commit()

    return {"token": token}