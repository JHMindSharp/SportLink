"""Add profile_completed to User model

Revision ID: 42f089d0ed91
Revises: 3b18c9f482e8
Create Date: 2024-10-31 16:14:45.646112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42f089d0ed91'
down_revision = '3b18c9f482e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_completed', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('email_confirmed', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('email_confirmed')
        batch_op.drop_column('profile_completed')

    # ### end Alembic commands ###