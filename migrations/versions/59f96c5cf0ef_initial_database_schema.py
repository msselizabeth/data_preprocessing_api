"""initial database schema

Revision ID: 59f96c5cf0ef
Revises: 
Create Date: 2026-11-07 10:11:21.554173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59f96c5cf0ef'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ApiClient
    op.create_table(
        'api_clients',
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("api_key_hash", sa.String(250), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False)
    )

    #JsonMappings
    op.create_table(
            'json_mappings',
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("token", sa.String(250), nullable=False, unique=True),
            sa.Column("mapping", sa.JSON(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("client_id", sa.Integer(), sa.ForeignKey("api_clients.id"), nullable=False)
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("json_mappings")
    op.drop_table("api_clients")
