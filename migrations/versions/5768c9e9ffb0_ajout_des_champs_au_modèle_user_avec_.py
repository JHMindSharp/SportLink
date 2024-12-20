"""Ajout des champs au modèle User avec contraintes nommées

Revision ID: 5768c9e9ffb0
Revises: b2de9ba8e112
Create Date: 2024-11-11 15:23:01.446544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5768c9e9ffb0'
down_revision = 'b2de9ba8e112'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('strava_id', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('facebook_id', sa.String(length=64), nullable=True))
        batch_op.create_unique_constraint('uq_user_facebook_id', ['facebook_id'])
        batch_op.create_unique_constraint('uq_user_strava_id', ['strava_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_strava_id', type_='unique')
        batch_op.drop_constraint('uq_user_facebook_id', type_='unique')
        batch_op.drop_column('facebook_id')
        batch_op.drop_column('strava_id')

    # ### end Alembic commands ###
