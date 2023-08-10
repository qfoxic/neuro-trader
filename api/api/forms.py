from pydantic import BaseModel
from .enums import ActivityTypeEnum, ChainTypeEnum


class ActivityForm(BaseModel):
    activity_type: ActivityTypeEnum
    token: str
    currency: str
    chain_type: ChainTypeEnum