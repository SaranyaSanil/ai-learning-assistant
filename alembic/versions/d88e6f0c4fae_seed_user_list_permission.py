"""seed user_list permission

Revision ID: d88e6f0c4fae
Revises: 8fbb1cc7bbf4
Create Date: 2026-06-17 13:50:14.916437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd88e6f0c4fae'
down_revision: Union[str, Sequence[str], None] = '8fbb1cc7bbf4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
