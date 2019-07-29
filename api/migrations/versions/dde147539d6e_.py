"""empty message

Revision ID: dde147539d6e
Revises: c1b93103c752
Create Date: 2019-08-21 13:00:14.245564

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = 'dde147539d6e'
down_revision = 'c1b93103c752'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('booking_invigilators',
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('invigilator_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['invigilator_id'], ['invigilator.invigilator_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('booking_id', 'invigilator_id')
    )
    op.add_column('booking', sa.Column('shadow_invigilator_id', sa.Integer(), nullable=True))
    op.add_column('invigilator', sa.Column('shadow_count', sa.Integer(), server_default='2', nullable=False))
    op.add_column('invigilator', sa.Column('shadow_flag', sa.String(length=1), server_default='Y', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking_invigilators')
    op.drop_column('invigilator', 'shadow_flag')
    op.drop_column('invigilator', 'shadow_count')
    op.drop_column('booking', 'shadow_invigilator_id')
    # ### end Alembic commands ###
