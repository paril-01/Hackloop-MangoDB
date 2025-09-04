"""initial migration

Revision ID: 0001_initial
Revises: 
Create Date: 2025-09-04 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=128), nullable=False, unique=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'activities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True, index=True),
        sa.Column('activity_type', sa.String(length=128), nullable=False, index=True),
        sa.Column('confidence', sa.Float(), nullable=False, default=0.0),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('details', sa.String(length=1024), nullable=True),
    )

    op.create_table(
        'automation_macros',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=256), nullable=False, index=True),
        sa.Column('description', sa.String(length=512), nullable=True),
        sa.Column('script', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('last_run_at', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_table('automation_macros')
    op.drop_table('activities')
    op.drop_table('users')
