"""empty message

Revision ID: 52e093d4a0ba
Revises: 2fe6aa3d40d2
Create Date: 2022-08-26 13:38:59.617101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52e093d4a0ba'
down_revision = '2fe6aa3d40d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('message_id', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_column('message_id')

    # ### end Alembic commands ###
