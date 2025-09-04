"""add user auth fields

Revision ID: 0003_add_user_auth_fields
Revises: 0002_initial
Create Date: 2025-09-04 00:10:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003_add_user_auth_fields'
down_revision = '0002_initial'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('password_hash', sa.String(length=256), nullable=True))
    op.add_column('users', sa.Column('failed_attempts', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('users', sa.Column('locked_until', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    op.drop_column('users', 'locked_until')
    op.drop_column('users', 'failed_attempts')
    op.drop_column('users', 'password_hash')
