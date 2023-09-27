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
    current_deposit = F.NumberField("CurrentDeposit")
    deposit_updated_at = F.CreatedTimeField("DepositUpdatedAt")
    monthly_profit = F.NumberField("MonthlyProfit")

    class Meta(BaseMeta):
        table_name = "users"


class Bots(Model):
    name = F.TextField("Name")
    user = F.LinkField("Users", Users, lazy=False)
    created_at = F.CreatedTimeField("CreatedAt")
    activity_type = F.SelectField("ActivityType")
    currency = F.TextField("Currency")
    chain_type = F.SelectField("ChainType")

    class Meta(BaseMeta):
        table_name = "bots"


class Transactions(Model):
    created_at = F.CreatedTimeField("CreatedAt")
    user = F.LinkField("User", Users, lazy=False)
    currency = F.TextField("Currency")
    chain_type = F.SelectField("ChainType")
    profit = F.NumberField("Profit")

    class Meta(BaseMeta):
        table_name = "transactions"
