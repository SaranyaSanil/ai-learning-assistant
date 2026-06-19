"""add composite pk to role_permissions

Revision ID: 8fbb1cc7bbf4
Revises: 1e97d903a340
Create Date: 2026-06-11 14:14:31.725805
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8fbb1cc7bbf4'
down_revision: Union[str, Sequence[str], None] = '1e97d903a340'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.alter_column(
        'role_permissions',
        'role_id',
        existing_type=sa.INTEGER(),
        nullable=False
    )

    op.alter_column(
        'role_permissions',
        'permission_id',
        existing_type=sa.INTEGER(),
        nullable=False
    )

    op.create_primary_key(
        "pk_role_permissions",
        "role_permissions",
        ["role_id", "permission_id"]
    )


def downgrade() -> None:

    op.drop_constraint(
        "pk_role_permissions",
        "role_permissions",
        type_="primary"
    )

    op.alter_column(
        'role_permissions',
        'permission_id',
        existing_type=sa.INTEGER(),
        nullable=True
    )

    op.alter_column(
        'role_permissions',
        'role_id',
        existing_type=sa.INTEGER(),
        nullable=True
    )