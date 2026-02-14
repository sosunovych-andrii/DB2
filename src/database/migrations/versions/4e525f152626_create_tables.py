"""create tables

Revision ID: 4e525f152626
Revises: 
Create Date: 2026-02-14 16:58:08.207712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e525f152626'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('manufacturers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('price_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unit_price', sa.DECIMAL(precision=15, scale=3), nullable=False),
    sa.Column('manufacturer_id', sa.Integer(), nullable=True),
    sa.Column('product_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['manufacturer_id'], ['manufacturers.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['product_type_id'], ['product_types.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_price_list_manufacturer_id'), 'price_list', ['manufacturer_id'], unique=False)
    op.create_index(op.f('ix_price_list_product_type_id'), 'price_list', ['product_type_id'], unique=False)
    op.create_table('sales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('sale_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('payment_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('price_list_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['price_list_id'], ['price_list.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sales_price_list_id'), 'sales', ['price_list_id'], unique=False)


def downgrade() -> None:
    op.drop_constraint('sales_ibfk_1', 'sales', type_='foreignkey')
    op.drop_index('ix_sales_price_list_id', table_name='sales')
    op.drop_table('sales')
    op.drop_constraint('price_list_ibfk_2', 'price_list', type_='foreignkey')
    op.drop_constraint('price_list_ibfk_1', 'price_list', type_='foreignkey')
    op.drop_index('ix_price_list_product_type_id', table_name='price_list')
    op.drop_index('ix_price_list_manufacturer_id', table_name='price_list')
    op.drop_table('price_list')
    op.drop_table('product_types')
    op.drop_table('manufacturers')
