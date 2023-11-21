"""init

Revision ID: 0f5ae4addbd2
Revises: 
Create Date: 2023-11-21 22:43:11.779739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f5ae4addbd2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("virtual_computer",
                    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                              nullable=True),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                              nullable=True),
                    sa.Column("v_ram", sa.Integer(), nullable=False),
                    sa.Column("v_cpu", sa.Integer(), nullable=False),
                    sa.Column("v_disk", sa.Integer(), nullable=False),
                    sa.Column("disk_id", sa.BigInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk__virtual_computer')),
                    sa.UniqueConstraint('id', name=op.f('uq__virtual_computer__id'))
                    )
    op.create_unique_constraint(op.f('uq__virtual_computer__disk_id'), 'virtual_computer', ['disk_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###