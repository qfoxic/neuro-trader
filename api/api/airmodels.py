import os
from pyairtable.orm import Model, fields as F


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
    initial_deposit = F.NumberField("InitialDeposit")

    class Meta(BaseMeta):
        table_name = "users"


class Bots(Model):
    name = F.TextField("Name")
    user = F.LinkField("Users", Users, lazy=False)
    created_at = F.CreatedTimeField("CreatedAt")
    activity_type = F.SelectField("ActivityType")
    currency = F.TextField("Currency")

    class Meta(BaseMeta):
        table_name = "bots"