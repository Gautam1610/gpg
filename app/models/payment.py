from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from enum import Enum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.customer import Customer


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"))
    currency: Mapped[str] = mapped_column(String(3))
    amount: Mapped[float] = mapped_column(Float)
    customer: Mapped["Customer"] = relationship(back_populates="payments")