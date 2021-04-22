"""add post image field

Revision ID: 08eb6c55819d
Revises: 73efcf27de2c
Create Date: 2021-04-21 20:21:46.840584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08eb6c55819d'
down_revision = '73efcf27de2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('image_file', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'image_file')
    # ### end Alembic commands ###
