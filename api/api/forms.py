from pydantic import BaseModel
from .enums import ActivityTypeEnum, ChainTypeEnum


class ActivityForm(BaseModel):
    activity_type: ActivityTypeEnum
    token: str
    currency: str
    chain_type: ChainTypeEnum


class UserDepositForm(BaseModel):
    token: str
    deposit: float


class UserTransactionForm(BaseModel):
    token: str
    profit: float
    currency: str
    chain_type: ChainTypeEnum
