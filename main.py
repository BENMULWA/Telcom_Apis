from fastapi import FastAPI
from handlers import handle_notification, handle_validation
from models import Notification, ValidationRequest


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}

@app.post("/c2b/notification")
async def c2b_notification(payload: Notification):
    return handle_notification(payload)

@app.post("/c2b/validation")
async def c2b_validation(payload: ValidationRequest):
    return handle_validation(payload)
