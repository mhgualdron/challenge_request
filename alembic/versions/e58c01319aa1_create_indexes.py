"""create_indexes

Revision ID: e58c01319aa1
Revises: e4b54c3d015d
Create Date: 2026-02-27 09:17:32.647875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e58c01319aa1'
down_revision: Union[str, Sequence[str], None] = 'e4b54c3d015d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('IX_Invoices_ClientName', 'invoices', ['client_name'], unique=False)


def downgrade() -> None:
    op.drop_index('IX_Invoices_ClientName', table_name='invoices')
