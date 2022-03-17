"""Handle pending rewards

Revision ID: 49b4b7cca932
Revises: 9c0ce1942023
Create Date: 2022-03-07 12:43:06.851616

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '49b4b7cca932'
down_revision = '9c0ce1942023'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_pending_rewards',
    sa.Column('row_id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('row_created', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('row_updated', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('airdrop_id', sa.BIGINT(), nullable=False),
    sa.Column('airdrop_window_id', sa.BIGINT(), nullable=False),
    sa.Column('address', sa.VARCHAR(length=50), nullable=False),
    sa.Column('pending_reward', sa.DECIMAL(precision=64, scale=0), nullable=False),
    sa.ForeignKeyConstraint(['airdrop_id'], ['airdrop.row_id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['airdrop_window_id'], ['airdrop_window.row_id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('row_id')
    )
    op.create_index(op.f('ix_user_pending_rewards_address'), 'user_pending_rewards', ['address'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_pending_rewards_address'), table_name='user_pending_rewards')
    op.drop_table('user_pending_rewards')
    # ### end Alembic commands ###
