"""Create constrains.

Revision ID: 18a13d4d91bc
Revises: ba6c6b87f789
Create Date: 2022-08-22 17:59:47.952226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18a13d4d91bc'
down_revision = 'ba6c6b87f789'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'companies', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'companies', type_='unique')
    # ### end Alembic commands ###
