"""Added speed_violation_count to AggregatedData model

Revision ID: dba25a6e1f9d
Revises: e1e69aa54202
Create Date: 2024-09-29 13:41:25.112941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dba25a6e1f9d'
down_revision = 'e1e69aa54202'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('aggregated_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('speed_violation_count', sa.Integer(), nullable=True))
        batch_op.drop_column('avg_speed_max')
        batch_op.drop_column('avg_speed_std')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('aggregated_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avg_speed_std', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('avg_speed_max', sa.FLOAT(), nullable=True))
        batch_op.drop_column('speed_violation_count')

    # ### end Alembic commands ###
