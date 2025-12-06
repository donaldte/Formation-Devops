from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

app = FastAPI(title="Auth Service")


class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "auth"}


@app.post("/register")
def register(user: UserRegister):
    # Simulation: on ne sauvegarde rien, on répond juste
    return {"message": "user registered (fake)", "user": user.email}


@app.post("/login")
def login(credentials: UserLogin):
    # Simulation: on renvoie un token bidon
    return {
        "access_token": "fake-jwt-token",
        "token_type": "bearer",
        "user": credentials.email,
    }


@app.on_event("startup")
async def _startup():
    Instrumentator().instrument(app).expose(app)