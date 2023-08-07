import datetime

from fastapi import APIRouter, HTTPException, status
from ..models.main import Users, UserStatusEnum

router = APIRouter()

@router.get("/verify/{token}")
async def verify_token(token: str):
    try:
        user = Users.from_id(token)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")

    if user.status == UserStatusEnum.Suspended.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is suspended")

    expire_at = user.subscription_expire_at

    if not expire_at:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="SubscriptionExpireAt not set")

    if (expire_at - datetime.date.today()).days <= 0:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Renew subscription")

    return "OK"
