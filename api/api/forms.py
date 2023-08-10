from pydantic import BaseModel
from .enums import ActivityTypeEnum


class ActivityForm(BaseModel):
    activity_type: ActivityTypeEnum
    token: str
    currency: str