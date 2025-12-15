from fastapi import FastAPI
from fastapi.responses import JSONResponse
from handlers import handle_notification, handle_validation, initiate_stk_push,handle_stk_callback, STKCallback
from models import Notification, ValidationRequest


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI is running successfully with status 200."}

@app.post("/c2b/notification")
async def c2b_notification(payload: Notification):
    return handle_notification(payload)

@app.post("/c2b/validation")
async def c2b_validation(payload: ValidationRequest):
    return handle_validation(payload)


# --- Initiate STK Push ---
@app.post("/stk/push")
async def stk_push(amount: float, msisdn: str, account_ref: str):
    """
    Initiates STK push to customer
    """
    callback_url = "https://https://telcom-apis.onrender.com/stk/callback"  # replace with your publicly accessible URL
    result = initiate_stk_push(amount, msisdn, account_ref, callback_url)
    return JSONResponse(content=result, status_code=200)


# --- STK Callback ---
@app.post("/stk/callback")
async def stk_callback(payload: STKCallback):
    """
    Receives STK Push result from Telkom
    """
    response = handle_stk_callback(payload)
    return JSONResponse(content=response, status_code=200)