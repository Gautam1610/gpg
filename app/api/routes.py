from app.schemas.customer import CreateCustomer
from app.schemas.payment import CreatePayment
from fastapi import Depends, HTTPException , Header
from app.models.customer import Customer
from app.models.payment import Payment
import shortuuid as uuid
from sqlalchemy.orm import Session
from app.db.session import get_db
import app.core.auth as auth
from app.schemas.merchant import MerchantRegister, MerchantLogin , TokenResponse
from app.models.merchant import Merchant
from fastapi import APIRouter
from jose import JWTError, jwt
from fastapi import Request , Body

router = APIRouter()

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/signup")
def signup(merchant: MerchantRegister, db: Session = Depends(get_db)):
    existing_merchant = db.query(Merchant).filter(Merchant.merchant_email == merchant.organization_mail).first()
    if existing_merchant:
        raise HTTPException(status_code=400, detail="Merchant already exists.")
    else:
        new_merchant = Merchant(
            id = str(uuid.uuid()),
            merchant_name=merchant.organization_name,
            merchant_email=merchant.organization_mail,
            hashed_password=auth.hash_pass(merchant.password)
        )
        db.add(new_merchant)
        db.commit()
        db.refresh(new_merchant)
        token = auth.create_access_token(data={"sub": new_merchant.id})
        return {
            "message": "✅ Merchant created successfully",
            "merchant_id": new_merchant.id,
            "access_token": token
        }

@router.post("/login")
async def login(merchant: MerchantLogin, db: Session = Depends(get_db)):
    existing_merchant = db.query(Merchant).filter(Merchant.merchant_email == merchant.organization_mail).first()
    if not existing_merchant:
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    if not auth.verify_pass(merchant.password, existing_merchant.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials.")
    
    token = auth.create_access_token(data={"sub": existing_merchant.id})
    return {
        "message": "✅ Merchant logged in successfully",
        "access_token": token
    }

def get_current_merchant(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Merchant:
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        merchant_id: str = payload.get("sub")
        if merchant_id is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)

    merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
    if merchant is None:
        raise HTTPException(status_code=401)
    return merchant

def verify_api_key(merchant_id : str , x_api_key : str = Header(...), db: Session = Depends(get_db)) -> Merchant:
    merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found.")
    if not merchant.hashed_key:
        raise HTTPException(status_code=401, detail="API key not found.")
    if not auth.verify_pass(x_api_key, merchant.hashed_key):
        raise HTTPException(status_code=401, detail="Invalid API key.")
    return merchant

def verify_api_key_from_customer(
    customer: CreateCustomer = Body(...),
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
) -> Merchant:
    merchant = db.query(Merchant).filter(Merchant.id == customer.merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found.")
    if not merchant.hashed_key:
        raise HTTPException(status_code=401, detail="API key not generated.")
    if not auth.verify_pass(x_api_key, merchant.hashed_key):
        raise HTTPException(status_code=401, detail="Invalid API key.")
    return merchant

    

@router.post("/generate-api-key")
def generate_api_key(
    current_merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    key, hashed = auth.create_api_key()

    current_merchant.hashed_key = hashed
    db.add(current_merchant) 
    db.commit()     
    db.refresh(current_merchant) 

    return {"api_key": key}


@router.post("/customer")
async def create_customer(
    customer: CreateCustomer,
    db: Session = Depends(get_db),
    current_merchant: Merchant = Depends(verify_api_key_from_customer)):
    existing_customer = db.query(Customer).filter(Customer.email == customer.email).first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer already exists.")

    new_customer = Customer(
        id=str(uuid.uuid()),
        merchant_id=current_merchant.id,
        name=customer.name,
        email=customer.email
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return {
        "message": "✅ Customer created successfully",
        "customer_id": new_customer.id
    }

def verify_api_key_from_payment(
    payment: CreatePayment = Body(...),
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
) -> Merchant:
    customer = db.query(Customer).filter(Customer.id == payment.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    merchant = db.query(Merchant).filter(Merchant.id == customer.merchant_id).first()
    if not merchant or not merchant.hashed_key:
        raise HTTPException(status_code=403, detail="Invalid merchant or missing API key.")

    if not auth.verify_pass(x_api_key, merchant.hashed_key):
        raise HTTPException(status_code=403, detail="Invalid API key.")

    return merchant


@router.post("/payment")
async def create_payment(payment: CreatePayment, db: Session = Depends(get_db),
                         current_merchant: Merchant = Depends(verify_api_key_from_payment)):
        customer = db.query(Customer).filter(Customer.id == payment.customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found.")
        if payment.amount <= 0:
            raise HTTPException(status_code=400, detail="Payment amount must be greater than zero.")
        new_payment = Payment(
            id = str(uuid.uuid()),
            amount=payment.amount,
            currency=payment.currency,
            customer_id=payment.customer_id
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)

        return {
            "message": "✅ Payment created successfully",
            "payment_id": new_payment.id
        }