"""add roles for users(default=user)

Revision ID: 9faaeb2f4b6b
Revises: 089e3f5f2c2f
Create Date: 2025-11-25 13:09:22.140416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9faaeb2f4b6b'
down_revision: Union[str, Sequence[str], None] = '089e3f5f2c2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('role', sa.String(), nullable=False, server_default='user'))


def downgrade() -> None:
    """Downgrade schema."""
    pass
