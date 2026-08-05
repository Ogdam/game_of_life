"""add rules column to sessions

Revision ID: 5ea441939c7c
Revises: ceda532fe8d5
Create Date: 2026-08-05 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "5ea441939c7c"
down_revision: Union[str, Sequence[str], None] = "ceda532fe8d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "sessions",
        sa.Column(
            "rules",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default='{"birth": [3], "survive": [2, 3]}',
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("sessions", "rules")
