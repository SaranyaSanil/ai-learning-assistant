"""seed role permissions

Revision ID: 1e97d903a340
Revises: 003437daee86
Create Date: 2026-06-11 10:46:31.582447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e97d903a340'
down_revision: Union[str, Sequence[str], None] = '003437daee86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # Super Admin gets ALL permissions
    op.execute("""
        INSERT INTO role_permissions (role_id, permission_id)
        SELECT r.id, p.id
        FROM roles r, permissions p
        WHERE r.name = 'Super Admin'
    """)

    # Moderator permissions
    op.execute("""
        INSERT INTO role_permissions (role_id, permission_id)
        SELECT r.id, p.id
        FROM roles r, permissions p
        WHERE LOWER(r.name) = 'moderator'
        AND p.name IN (
            'USER_VIEW',
            'USER_UPDATE',
            'USER_LIST',
            'ROLE_VIEW'
        )
    """)

    # User permissions
    op.execute("""
        INSERT INTO role_permissions (role_id, permission_id)
        SELECT r.id, p.id
        FROM roles r, permissions p
        WHERE LOWER(r.name) = 'user'
        AND p.name IN (
            'USER_VIEW'
        )
    """)


def downgrade():
    op.execute("""
        DELETE FROM role_permissions
        WHERE (role_id, permission_id) IN (

            SELECT r.id, p.id
            FROM roles r, permissions p
            WHERE r.name = 'Super Admin'

            UNION

            SELECT r.id, p.id
            FROM roles r, permissions p
            WHERE LOWER(r.name) = 'moderator'
            AND p.name IN (
                'USER_VIEW',
                'USER_UPDATE',
                'USER_LIST',
                'ROLE_VIEW'
            )

            UNION

            SELECT r.id, p.id
            FROM roles r, permissions p
            WHERE LOWER(r.name) = 'user'
            AND p.name IN (
                'USER_VIEW'
            )
        )
    """)
