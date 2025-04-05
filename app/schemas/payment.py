from app.schemas.base import BaseModel



class CreatePayment(BaseModel):
    amount: float
    currency: str
    customer_id: str
    status: str