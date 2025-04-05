from app.schemas.base import BaseModel
from enum import Enum


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    INR = "INR"

class CreatePayment(BaseModel):
    amount: float
    currency: Currency
    customer_id: str
    status: str