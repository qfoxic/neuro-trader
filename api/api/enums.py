from enum import Enum


class UserStatusEnum(str, Enum):
    Active = "Active"
    Suspended = "Suspended"
    Testing = "Testing"


class ActivityTypeEnum(str, Enum):
    StartBuy = "Start Buy"
    StartSell = "Start Sell"
    PartialBuy = "Partial Buy"
    PartialSell = "Partial Sell"
    FullLockBuy = "Full Lock Buy"
    FullLockSell = "Full Lock Sell"
    AntiLockBuy = "Anti Lock Buy"
    AntiLockSell = "Anti Lock Sell"
    TrailingsBuy = "Trailings Buy"
    TrailingsSell = "Trailings Sell"
