"""empty message

Revision ID: 253213ee0514
Revises: 3fe0bbe78251
Create Date: 2023-03-02 18:03:21.388499

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '253213ee0514'
down_revision = '3fe0bbe78251'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=True))
        batch_op.drop_column('quantity_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###