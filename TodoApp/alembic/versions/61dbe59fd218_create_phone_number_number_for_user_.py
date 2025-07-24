"""Create phone number_number for user column

Revision ID: 61dbe59fd218
Revises: 
Create Date: 2025-07-18 14:19:19.206914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61dbe59fd218'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("phone_number", sa.String(), nullable=True),)
    pass


def downgrade() -> None:
    op.drop_column("users", "phone_number")
    pass
