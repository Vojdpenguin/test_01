from fastapi import FastAPI
from src.credits.routers import router as contacts_router

app = FastAPI()

app.include_router(contacts_router, prefix="/credits", tags=["credits"])

@app.get("/ping")
async def ping():
    return {"message": "pong"}
