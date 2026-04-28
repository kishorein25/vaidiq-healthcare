from fastapi import APIRouter
from app.database import SessionLocal
from app.models import User, Doctor
from app.auth import hash_password

router = APIRouter(prefix="/doctor")

@router.post("/register")
def register_doctor(name: str, email: str, password: str, gov_id: str):
    db = SessionLocal()

    user = User(
        name=name,
        email=email,
        password=hash_password(password),
        role="doctor"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    doctor = Doctor(
        user_id=user.id,
        gov_id_number=gov_id,
        is_verified=False
    )
    db.add(doctor)
    db.commit()

    return {"msg": "Doctor registered, waiting for admin approval"}