from fastapi import APIRouter
from app.database import SessionLocal
from app.models import User, Patient
from app.auth import hash_password

router = APIRouter(prefix="/patient")

@router.post("/register")
def register_patient(name: str, email: str, password: str):
    db = SessionLocal()

    user = User(
        name=name,
        email=email,
        password=hash_password(password),
        role="patient"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    patient = Patient(user_id=user.id)
    db.add(patient)
    db.commit()

    return {"msg": "Patient registered"}