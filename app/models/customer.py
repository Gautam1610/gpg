from __future__ import annotations 
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from app.db.base import Base
if TYPE_CHECKING:
    from app.models.payment import Payment


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)

    payments: Mapped[list["Payment"]] = relationship(back_populates="customer")
