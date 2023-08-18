import datetime

from fastapi import APIRouter, HTTPException, status
from pyairtable.formulas import match
from .enums import UserStatusEnum
from .airmodels import Users, Bots, Transactions
from .forms import ActivityForm, UserDepositForm, UserTransactionForm


router = APIRouter()


@router.post("/verify/{token}")
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


@router.post("/bots")
async def create_activity(activity: ActivityForm):
    try:
        user = Users.from_id(activity.token)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    botActivity = Bots(
        activity_type=activity.activity_type,
        user=[user],
        currency=activity.currency,
        chain_type=activity.chain_type
    )
    botActivity.save()
    return "OK"


@router.post("/bots/clear")
async def delete_user_activities(activity: ActivityForm):
    try:
        user = Users.from_id(activity.token)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    botActivities = Bots.all(
        formula=match({"Users": user.name, "Currency": activity.currency, "ChainType": activity.chain_type.value})
    )
    Bots.batch_delete(botActivities)
    return "OK"


@router.post("/bots/deposit")
async def update_user_deposit(userDeposit: UserDepositForm):
    try:
        user = Users.from_id(userDeposit.token)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not user.initial_deposit:
        user.initial_deposit = userDeposit.deposit
        user.current_deposit = userDeposit.deposit
        user.save()
    elif user.deposit_updated_at.month != datetime.datetime.now().month:
        user.monthly_profit = userDeposit.deposit - user.current_deposit
        user.current_deposit = userDeposit.deposit
        user.save()
    return "OK"


@router.post("/bots/transactions")
async def add_bot_transaction(userTransaction: UserTransactionForm):
    try:
        user = Users.from_id(userTransaction.token)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    transaction = Transactions(
        user = [user],
        currency = userTransaction.currency,
        chain_type = userTransaction.chain_type,
        profit = userTransaction.profit
    )
    transaction.save()
    return "OK"