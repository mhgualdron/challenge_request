"""seed_data

Revision ID: b4d0c197b3d3
Revises: 34e79cf95f61
Create Date: 2026-02-27 09:18:22.576749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4d0c197b3d3'
down_revision: Union[str, Sequence[str], None] = '34e79cf95f61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    EXEC sp_CreateInvoice 'INV-001', 'Acme Corp', 'C-001', 1500.00, 'COP', '2026-01-01', '2026-02-01', 'PAID', 'Initial seed invoice';
    EXEC sp_CreateInvoice 'INV-002', 'Globex', 'C-002', 2500.50, 'COP', '2026-02-15', NULL, 'PENDING', 'Pending service fee';
    EXEC sp_CreateInvoice 'INV-003', 'Soylent Corp', 'C-003', 500.00, 'USD', '2026-02-20', '2026-03-20', 'PENDING', 'Monthly subscription';
    """)


def downgrade() -> None:
    op.execute("DELETE FROM invoices WHERE invoice_number IN ('INV-001', 'INV-002', 'INV-003')")
