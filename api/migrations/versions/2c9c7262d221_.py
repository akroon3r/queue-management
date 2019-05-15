"""empty message

Revision ID: 2c9c7262d221
Revises: 3a98e5395000
Create Date: 2019-05-15 10:16:23.063868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c9c7262d221'
down_revision = '3a98e5395000'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invigilator', sa.Column('deleted', sa.DateTime(), nullable=True))
    op.add_column('room', sa.Column('deleted', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('room', 'deleted')
    op.drop_column('invigilator', 'deleted')
    # ### end Alembic commands ###
