"""add timestamps to todos

Revision ID: 832651e1971d
Revises: 3f42cf887c5b
Create Date: 2026-09-07 11:15:14.643437

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "832651e1971d"
down_revision: Union[str, Sequence[str], None] = "3f42cf887c5b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    with op.batch_alter_table("todos") as batch_op:
        batch_op.add_column(
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                nullable=True,
            )
        )

    # 既存Todoに現在時刻を設定
    op.execute(
        sa.text(
            "UPDATE todos SET updated_at = CURRENT_TIMESTAMP "
            "WHERE updated_at IS NULL"
        )
    )

    with op.batch_alter_table("todos") as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(timezone=True),
            nullable=False,
        )


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table("todos") as batch_op:
        batch_op.drop_column("updated_at")