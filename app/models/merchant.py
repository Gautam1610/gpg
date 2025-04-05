from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from enum import Enum
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.customer import Customer

class Merchant(Base):
    __tablename__ = "merchants"
    id : Mapped[str] = mapped_column(String, primary_key=True, index=True)
    merchant_name: Mapped[str] = mapped_column(String(100), unique=True)
    merchant_email: Mapped[str] = mapped_column(String(100), unique=True)
    registered_customer: Mapped[List["Customer"]] = relationship(
        back_populates="merchant" , cascade="all, delete-orphan"
        )