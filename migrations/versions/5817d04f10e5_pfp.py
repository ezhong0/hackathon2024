"""pfp

Revision ID: 5817d04f10e5
Revises: 1d8afcfb84d2
Create Date: 2024-08-03 19:11:35.510002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5817d04f10e5'
down_revision = '1d8afcfb84d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_photo', sa.String(length=256), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('profile_photo')

    # ### end Alembic commands ###
