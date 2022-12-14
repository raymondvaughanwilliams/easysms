"""empty message

Revision ID: dd2f70497eed
Revises: 8ac0c2bc83d9
Create Date: 2022-08-12 15:54:27.125341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd2f70497eed'
down_revision = '8ac0c2bc83d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('packages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=False),
    sa.Column('amount', sa.Text(), nullable=False),
    sa.Column('features', sa.Text(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_packages'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('packages')
    # ### end Alembic commands ###
