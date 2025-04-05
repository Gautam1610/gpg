from app.schemas.customer import CreateCustomer
from app.schemas.payment import CreatePayment
from fastapi import Depends, HTTPException
from app.models.customer import Customer
from app.models.payment import Payment
import shortuuid as uuid
from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi import APIRouter

router = APIRouter()

@router.post("/customer")
async def create_customer(customer: CreateCustomer, db: Session = Depends(get_db)):
    existing_customer = db.query(Customer).filter(Customer.email == customer.email).first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer already exists.")

    new_customer = Customer(
        id = str(uuid.uuid()),
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


@router.post("/payment")
async def create_payment(payment: CreatePayment, db: Session = Depends(get_db)):
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