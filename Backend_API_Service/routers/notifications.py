from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)

class NotificationBase(BaseModel):
    recipient_email: EmailStr = Field(..., description="Recipient email for notification")
    message: str = Field(..., description="Notification message content")

class NotificationSend(NotificationBase):
    channel: str = Field("email", description="Notification channel: email or sms")

class NotificationResponse(NotificationBase):
    status: str = Field(..., description="Delivery status")
    delivery_id: int = Field(..., description="Notification delivery ID")

# Simulated notifications log for scaffolding purposes
_fake_notifications_db = {}

# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send a notification",
    description="Send an email or SMS notification to a user.",
    responses={400: {"description": "Invalid notification data."}},
)
def send_notification(notification: NotificationSend):
    """
    Send a notification (email/SMS) to a user.
    """
    delivery_id = len(_fake_notifications_db) + 1
    _fake_notifications_db[delivery_id] = notification.dict() | {"delivery_id": delivery_id, "status": "delivered"}
    return NotificationResponse(
        recipient_email=notification.recipient_email,
        message=notification.message,
        channel=notification.channel,
        delivery_id=delivery_id,
        status="delivered"
    )

# PUBLIC_INTERFACE
@router.get(
    "/{delivery_id}",
    response_model=NotificationResponse,
    summary="Get notification by delivery ID",
    description="Fetch details of a previously sent notification by delivery id.",
    responses={404: {"description": "Notification not found."}},
)
def get_notification(delivery_id: int):
    """
    Get notification delivery details by delivery ID.
    """
    notif = _fake_notifications_db.get(delivery_id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found.")
    return NotificationResponse(**notif)
