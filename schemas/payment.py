from datetime import datetime

from aiogram.types import SuccessfulPayment, User
from pydantic import Field

from pydantic import BaseModel, ConfigDict

from .obj_id import PyObjectId


class CreateSuccessfulPaymentSchema(BaseModel):
    successful_payment: SuccessfulPayment
    from_user: User
    time_created: datetime


class PaymentSchema(CreateSuccessfulPaymentSchema):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: PyObjectId = Field(alias='_id')
