"""ClaimHistory

Revision ID: 1c6bb2fd25d5
Revises: 7369cbf41001
Create Date: 2021-12-17 14:46:59.852877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c6bb2fd25d5'
down_revision = '7369cbf41001'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('claim_history', sa.Column('type', sa.VARCHAR(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('claim_history', 'type')
    # ### end Alembic commands ###
