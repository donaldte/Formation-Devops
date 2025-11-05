from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🚀 Votre application fonctionne sur Docker Compose V2 !"}

@app.get("/health")
def health():
    return {"status": "ok"}
