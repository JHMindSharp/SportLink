"""Ajout de champs supplémentaires au modèle User

Revision ID: 85af6402b26e
Revises: 424bfa40a84b
Create Date: 2024-11-01 17:03:55.992694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85af6402b26e'
down_revision = '424bfa40a84b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sport',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rater_id', sa.Integer(), nullable=False),
    sa.Column('rated_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['rated_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['rater_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_sports',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('sport_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['sport_id'], ['sport.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'sport_id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content_type', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('title', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('subtitle', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('image', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('video', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('music', sa.String(length=255), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cover_image', sa.String(length=255), nullable=True))
        batch_op.alter_column('profile_image',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('profile_image',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=128),
               existing_nullable=True)
        batch_op.drop_column('cover_image')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('music')
        batch_op.drop_column('video')
        batch_op.drop_column('image')
        batch_op.drop_column('subtitle')
        batch_op.drop_column('title')
        batch_op.drop_column('content_type')

    op.drop_table('user_sports')
    op.drop_table('rating')
    op.drop_table('sport')
    # ### end Alembic commands ###
