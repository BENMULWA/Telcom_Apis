from pydantic import BaseModel
from typing import Optional

# --- Notification Models that confirms payment received after payment---
class NotificationURL(BaseModel):
    billerId: str
    brandName: str
    transactionDate: str
    accountNumber: str
    transactionId: str
    destinationFees: Optional[str] = None
    accountId: Optional[str] = None
    transactionFee: Optional[str] = None
    sourceMSISDN: str
    transactionAmount: str
    brandId: Optional[str] = None
    accBalance: Optional[str] = None
    accountBalance: Optional[str] = None
    billerMsisdn: Optional[str] = None
    srcAccountName: Optional[str] = None
    destAccName: Optional[str] = None
    txnTime: Optional[str] = None
    customersIDdocumentType: Optional[str] = None
    customersIDdocumentNumber: Optional[str] = None

class Notification(BaseModel):
    notificationType: str
    notificationBody: NotificationURL


# --- Validation Models ---
class ValidationBody(BaseModel):
    signature: Optional[str] = None
    sourceMsisdn: str
    billerAccountNo: str
    sourceName: str
    billerId: str
    billerMsisdn: Optional[str] = None
    amount: str
    regDocType: Optional[str] = None
    idNumber: Optional[str] = None
    Info1: Optional[str] = None

class ValidationRequest(BaseModel):
    validationType: str
    validationBody: ValidationBody


# --- Validation Response ---
class BillerValidationRespond(BaseModel):
    userBalance: Optional[str] = ""
    resultMessage: str
    resultCode: int
    info1: Optional[str] = ""
    dueDate: Optional[str] = ""
    amountOwed: Optional[str] = ""
    accountNum: Optional[str] = ""

class ValidationResponse(BaseModel):
    billerValidationRespond: BillerValidationRespond

