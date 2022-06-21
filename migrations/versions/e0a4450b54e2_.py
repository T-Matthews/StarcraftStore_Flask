"""empty message

Revision ID: e0a4450b54e2
Revises: 390dc2125598
Create Date: 2022-06-21 10:52:01.835659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0a4450b54e2'
down_revision = '390dc2125598'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'units', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'units', type_='unique')
    # ### end Alembic commands ###