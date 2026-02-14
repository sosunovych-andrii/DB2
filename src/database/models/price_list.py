from sqlalchemy import Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.database.models.base import Base


class PriceListModel(Base):
    __tablename__ = "price_list"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    unit_price: Mapped[float] = mapped_column(
        DECIMAL(15, 3),
        nullable=False
    )

    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="manufacturers.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )
    product_type_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="product_types.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )
