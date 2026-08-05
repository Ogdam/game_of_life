"""create sessions table

Revision ID: ceda532fe8d5
Revises:
Create Date: 2026-08-05 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "ceda532fe8d5"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "sessions",
        sa.Column("client_id", sa.String(length=64), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False, server_default="90"),
        sa.Column("height", sa.Integer(), nullable=False, server_default="90"),
        sa.Column(
            "state", sa.String(length=16), nullable=False, server_default="pause"
        ),
        sa.Column("speed", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("tick", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "grid",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default="[]",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("client_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("sessions")
