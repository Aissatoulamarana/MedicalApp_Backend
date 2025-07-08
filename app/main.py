
from fastapi import FastAPI
from app.user.routes import router as user_router
from app.auth.routes import router as auth_router
from app.hospital.routes import router as hospital_router
from app.doctor.routes import router as doctor_router
from app.core.database import init_db



app = FastAPI(
    title="Medical Appointment API",
    version='1.0.0'
)


@app.on_event('startup')
def on_startup():
    init_db()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(hospital_router)
app.include_router(doctor_router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur la documentation de l'api medical app "}