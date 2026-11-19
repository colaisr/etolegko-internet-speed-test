"""stream published snapshots

Revision ID: b8f2c1d4e9a0
Revises: d17470a1261a
Create Date: 2026-11-19 12:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "b8f2c1d4e9a0"
down_revision: Union[str, None] = "d17470a1261a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stream_published_snapshots",
        sa.Column("stream_id", sa.Uuid(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["stream_id"], ["streams.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("stream_id"),
    )


def downgrade() -> None:
    op.drop_table("stream_published_snapshots")