from fastapi.responses import JSONResponse
from models import NotificationURL, ValidationRequest, ValidationResponse, BillerValidationRespond
import datetime
import requests
from typing import Optional

# -------------------------------
# --- Notification Handler ---
# -------------------------------
def handle_notification(payload: NotificationURL):
    body = payload

    # Example: log or save the payment
    print(f"Received payment for account {body.accountNumber} amount {body.transactionAmount}")

    # TODO: persist transaction in DB

    # Return acknowledgment
    return {
        "status": "SUCCESS",
        "message": "Payment received and processed"
    }


# -------------------------------
# --- Validation Handler ---
# -------------------------------
def handle_validation(payload: ValidationRequest):
    account_no = payload.validationBody.billerAccountNo

    if account_no == "123":
        response = ValidationResponse(
            billerValidationRespond=BillerValidationRespond(
                userBalance="5000.00",
                resultMessage="Account found",
                resultCode=0,
                info1="Valid account",
                dueDate=(datetime.date.today() + datetime.timedelta(days=30)).isoformat(),
                amountOwed="0.00",
                accountNum=account_no
            )
        )
    else:
        response = ValidationResponse(
            billerValidationRespond=BillerValidationRespond(
                userBalance="",
                resultMessage="Account not found",
                resultCode=99,
                info1="",
                dueDate="",
                amountOwed="",
                accountNum=account_no
            )
        )

    return JSONResponse(content=response.dict(), status_code=200)


# -------------------------------
# --- STK Push Handler ---
# -------------------------------
TELKOM_STK_URL = "https://api.telkom.co.ke/stkpush"  # replace with actual endpoint
TELKOM_CONSUMER_KEY = "YOUR_CONSUMER_KEY"
TELKOM_CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"

def initiate_stk_push(amount: float, msisdn: str, account_ref: str, callback_url: str):
    """
    Initiates STK push for a customer.
    """
    payload = {
        "amount": str(amount),
        "msisdn": msisdn,
        "accountReference": account_ref,
        "callbackURL": callback_url,
        "description": f"Payment for {account_ref}"
    }

    # Auth example (if Telkom uses Basic Auth)
    auth = (TELKOM_CONSUMER_KEY, TELKOM_CONSUMER_SECRET)

    try:
        resp = requests.post(TELKOM_STK_URL, json=payload, auth=auth, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {"error": f"STK Push failed: {str(e)}"}


# -------------------------------
# --- STK Callback Handler ---
# -------------------------------
from pydantic import BaseModel

class STKCallback(BaseModel):
    transactionId: str
    amount: str
    msisdn: str
    accountReference: str
    resultCode: int
    resultDesc: str

def handle_stk_callback(payload: STKCallback):
    # Log callback
    print(f"STK Callback received: {payload.transactionId} - {payload.resultDesc} - {payload.amount}")

    # TODO: Save transaction to DB, mark success/failure
    # Example:
    if payload.resultCode == 0:
        status = "SUCCESS"
    else:
        status = "FAILED"

    print(f"Transaction {payload.transactionId} status: {status}")
    return {"status": "received"}
