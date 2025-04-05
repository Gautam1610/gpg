from app.schemas.base import BaseModel
from pydantic import EmailStr

class MerchantRegister(BaseModel):
    organization_name: str
    organization_mail : EmailStr