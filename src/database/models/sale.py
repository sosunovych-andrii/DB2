from datetime import datetime

from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class SaleModel(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    sale_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    payment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    price_list_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="price_list.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )
