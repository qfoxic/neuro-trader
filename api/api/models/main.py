import os
from enum import Enum
from pyairtable.orm import Model, fields as F


class UserStatusEnum(Enum):
    Active = "Active"
    Suspended = "Suspended"
    Testing = "Testing"


class BaseMeta:
    @staticmethod
    def api_key():
        return os.environ["AIRTABLE_API_KEY"]

    @staticmethod
    def base_id():
        return os.environ["AIRTABLE_BASE_ID"]


class Groups(Model):
    name = F.TextField("Name")

    class Meta(BaseMeta):
        table_name = "groups"


class Users(Model):
    name = F.TextField("Name")
    token = F.TextField("Token", readonly=True)
    created_at = F.CreatedTimeField("CreatedAt")
    status = F.SelectField("Status")
    group = F.LinkField("Group", Groups, lazy=False)
    subscription_expire_at = F.DateField("SubscriptionExpireAt")

    class Meta(BaseMeta):
        table_name = "users"
