from app.schemas.base import BaseModel
from pydantic import EmailStr


class CreateCustomer(BaseModel):
    name : str
    email : EmailStr
    merchant_id : str

