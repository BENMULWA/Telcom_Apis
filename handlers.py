from fastapi.responses import JSONResponse
from models import NotificationURL, ValidationRequest, ValidationResponse, BillerValidationRespond
import datetime

# --- Notification Handler ---
def handle_notification(payload: NotificationURL):
    tx = payload.notificationBody
    print(f"Notification received: txID={tx.transactionId}, amount={tx.transactionAmount}, src={tx.sourceMSISDN}")
    return JSONResponse(content={"status": "success"}, status_code=200)

# --- Validation Handler ---
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
