"""empty message

Revision ID: 2402e67f7b4e
Revises: ebdba1df5644
Create Date: 2023-01-27 11:19:31.840940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2402e67f7b4e'
down_revision = 'ebdba1df5644'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('topups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('transaction_id', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('reference', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('topups', schema=None) as batch_op:
        batch_op.drop_column('reference')
        batch_op.drop_column('transaction_id')
        batch_op.drop_column('status')

    # ### end Alembic commands ###
