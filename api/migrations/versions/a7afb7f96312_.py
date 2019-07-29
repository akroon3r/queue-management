"""empty message

Revision ID: a7afb7f96312
Revises: c1b93103c752
Create Date: 2019-08-06 11:20:55.987933

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = 'a7afb7f96312'
down_revision = 'c1b93103c752'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invigilator', sa.Column('shadow_count', sa.Integer(), nullable=False))
    op.add_column('invigilator', sa.Column('shadow_flag', sa.String(length=1), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('invigilator', 'shadow_flag')
    op.drop_column('invigilator', 'shadow_count')
    # ### end Alembic commands ###
