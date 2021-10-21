"""empty message

Revision ID: 3458360ac451
Revises: d3a92c54d67a
Create Date: 2021-10-21 00:31:54.484365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3458360ac451'
down_revision = 'd3a92c54d67a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('gender', sa.String(length=80), nullable=False),
    sa.Column('hair_color', sa.String(length=80), nullable=False),
    sa.Column('eye_color', sa.String(length=80), nullable=False),
    sa.Column('height', sa.String(length=80), nullable=False),
    sa.Column('mass', sa.String(length=80), nullable=False),
    sa.Column('skin_color', sa.String(length=80), nullable=False),
    sa.Column('birth_year', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('character')
    # ### end Alembic commands ###
