"""add posts view counter

Revision ID: 496982c3f7ab
Revises: 08eb6c55819d
Create Date: 2021-04-23 10:31:42.105556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '496982c3f7ab'
down_revision = '08eb6c55819d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'posts',
        sa.Column(
            'views_counter',
            sa.Integer(),
            nullable=False,
            server_default="0"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'views_counter')
    # ### end Alembic commands ###
