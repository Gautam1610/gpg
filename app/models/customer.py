from __future__ import annotations 
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.merchant import Merchant
from typing import TYPE_CHECKING

from app.db.base import Base
if TYPE_CHECKING:
    from app.models.payment import Payment
    from app.models.merchant import Merchant


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    merchant_id: Mapped[str] = mapped_column(ForeignKey("merchants.id"))
    payments: Mapped[list["Payment"]] = relationship(back_populates="customer")
    merchant: Mapped["Merchant"] = relationship(back_populates="registered_customer")
