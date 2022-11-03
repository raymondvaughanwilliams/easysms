"""empty message

Revision ID: d46e8de99fdd
Revises: 48dc38a5fa08
Create Date: 2022-11-02 00:02:42.269299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd46e8de99fdd'
down_revision = '48dc38a5fa08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mnotify', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('routesms', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('routesms')
        batch_op.drop_column('mnotify')

    # ### end Alembic commands ###