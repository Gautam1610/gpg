from app.schemas.base import BaseModel
from pydantic import EmailStr

class MerchantRegister(BaseModel):
    organization_name: str
    organization_mail : EmailStr
    password: str

class MerchantLogin(BaseModel):
    organization_mail : EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class APIKeyResponse(BaseModel):
    api_key: str