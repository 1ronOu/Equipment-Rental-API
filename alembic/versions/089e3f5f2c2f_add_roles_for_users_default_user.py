"""add roles for users(default=user)

Revision ID: 089e3f5f2c2f
Revises: 396c3772fa07
Create Date: 2025-11-25 13:07:57.260235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '089e3f5f2c2f'
down_revision: Union[str, Sequence[str], None] = '396c3772fa07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
