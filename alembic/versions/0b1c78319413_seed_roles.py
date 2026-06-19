"""seed roles

Revision ID: 0b1c78319413
Revises: 8f92de088084
Create Date: 2026-06-02 09:06:38.007562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b1c78319413'
down_revision: Union[str, Sequence[str], None] = '8f92de088084'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        INSERT INTO roles (name)
        VALUES
        ('Super Admin'),
        ('User'),
        ('Moderator')
    """)

def downgrade():
    op.execute("""
        DELETE FROM roles
        WHERE name IN ('Super Admin', 'User', 'Moderator')
    """)