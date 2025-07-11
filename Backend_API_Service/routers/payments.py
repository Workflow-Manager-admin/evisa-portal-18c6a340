from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)

class PaymentBase(BaseModel):
    application_id: int = Field(..., description="Related visa application ID")
    user_id: int = Field(..., description="User making the payment")
    amount: float = Field(..., gt=0, description="Payment amount in FJD")

class PaymentCreate(PaymentBase):
    method: str = Field(..., description="Payment method (card, mpaisa, etc)")

class PaymentResponse(PaymentBase):
    payment_id: int = Field(..., description="Payment transaction ID")
    status: str = Field(..., description="Status of the payment (pending, completed, failed)")
    transaction_time: str = Field(..., description="ISO8601 timestamp of transaction")

# Simulated payments storage for scaffolding (replace with real service layer)
_fake_payments_db = {}

from datetime import datetime

# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record a payment for a visa application",
    description="Record payment initiation or completion for a visa application.",
    responses={400: {"description": "Invalid payment or double transaction."}},
)
def create_payment(payment: PaymentCreate):
    """
    Record a payment for a visa application.
    """
    payt_id = len(_fake_payments_db) + 1
    now_str = datetime.utcnow().isoformat() + "Z"
    payment_data = payment.dict() | {"payment_id": payt_id, "status": "completed", "transaction_time": now_str}
    _fake_payments_db[payt_id] = payment_data
    return PaymentResponse(**payment_data)

# PUBLIC_INTERFACE
@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
    summary="Get payment by ID",
    description="Fetch payment transaction details by its transaction ID.",
    responses={404: {"description": "Payment not found."}},
)
def get_payment(payment_id: int):
    """
    Get payment transaction details by payment ID.
    """
    payt = _fake_payments_db.get(payment_id)
    if not payt:
        raise HTTPException(status_code=404, detail="Payment not found.")
    return PaymentResponse(**payt)
