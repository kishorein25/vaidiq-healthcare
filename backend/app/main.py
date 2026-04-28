from fastapi import FastAPI
from app.database import Base, engine

from app.routes import doctor, admin, patient, queue

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MediQueue SaaS")

app.include_router(doctor.router)
app.include_router(admin.router)
app.include_router(patient.router)
app.include_router(queue.router)