"""seed permissions

Revision ID: 003437daee86
Revises: cfd99d7a8635
Create Date: 2026-06-11 10:45:41.291393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003437daee86'
down_revision: Union[str, Sequence[str], None] = 'cfd99d7a8635'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.execute("""
        INSERT INTO permissions (name)
        VALUES
        ('USER_VIEW'),
        ('USER_CREATE'),
        ('USER_UPDATE'),
        ('USER_DELETE'),
        ('USER_LIST'),

        ('ROLE_VIEW'),
        ('ROLE_CREATE'),
        ('ROLE_DELETE'),

        ('ASSIGN_ROLE'),
        ('MANAGE_PERMISSIONS')
    """)

def downgrade():
    op.execute("""
        DELETE FROM permissions
        WHERE name IN (
            'USER_VIEW',
            'USER_CREATE',
            'USER_UPDATE',
            'USER_DELETE',
            'USER_LIST',
            'ROLE_VIEW',
            'ROLE_CREATE',
            'ROLE_DELETE',
            'ASSIGN_ROLE',
            'MANAGE_PERMISSIONS'
        )
    """)