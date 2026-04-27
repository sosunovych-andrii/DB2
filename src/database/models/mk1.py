from datetime import date
from typing import Optional, List
from sqlalchemy import Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base

class FirmModel(Base):
    __tablename__ = "firms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(500))
    edrpou: Mapped[str] = mapped_column(String(10), unique=True)

    orders: Mapped[List["OrderModel"]] = relationship(back_populates="firm")


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True) # Номер замовлення
    firm_id: Mapped[int] = mapped_column(
        ForeignKey("firms.id", ondelete="CASCADE"),
        index=True
    )
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    payment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    firm: Mapped["FirmModel"] = relationship(back_populates="orders")
    contents: Mapped[List["OrderContentModel"]] = relationship(back_populates="order")


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True) # Код товару
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    order_contents: Mapped[List["OrderContentModel"]] = relationship(back_populates="product")


class OrderContentModel(Base):
    __tablename__ = "order_contents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="RESTRICT"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    order: Mapped["OrderModel"] = relationship(back_populates="contents")
    product: Mapped["ProductModel"] = relationship(back_populates="order_contents")
