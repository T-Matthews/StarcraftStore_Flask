"""empty message

Revision ID: b8f0bb240958
Revises: e0a4450b54e2
Create Date: 2022-06-21 11:47:11.536461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8f0bb240958'
down_revision = 'e0a4450b54e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('api_token', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'api_token')
    # ### end Alembic commands ###