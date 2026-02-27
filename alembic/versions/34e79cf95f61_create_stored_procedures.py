"""create_stored_procedures

Revision ID: 34e79cf95f61
Revises: e58c01319aa1
Create Date: 2026-02-27 09:17:50.921830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34e79cf95f61'
down_revision: Union[str, Sequence[str], None] = 'e58c01319aa1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # sp_CreateInvoice
    op.execute("""
    CREATE PROCEDURE sp_CreateInvoice
        @InvoiceNumber VARCHAR(50),
        @ClientName VARCHAR(150),
        @ClientID VARCHAR(50),
        @TotalAmount DECIMAL(18,2),
        @Currency VARCHAR(3),
        @IssueDate DATE,
        @DueDate DATE = NULL,
        @Status VARCHAR(20) = 'PENDING',
        @Description TEXT = NULL
    AS
    BEGIN
        SET NOCOUNT ON;
        BEGIN TRY
            INSERT INTO invoices (invoice_number, client_name, client_id, total_amount, currency, issue_date, due_date, status, description)
            OUTPUT inserted.*
            VALUES (@InvoiceNumber, @ClientName, @ClientID, @TotalAmount, @Currency, @IssueDate, @DueDate, @Status, @Description);
        END TRY
        BEGIN CATCH
            THROW;
        END CATCH
    END
    """)

    # sp_GetInvoiceById
    op.execute("""
    CREATE PROCEDURE sp_GetInvoiceById
        @ID INT
    AS
    BEGIN
        SET NOCOUNT ON;
        SELECT * FROM invoices WHERE id = @ID;
    END
    """)

    # sp_SearchInvoicesByClient
    op.execute("""
    CREATE PROCEDURE sp_SearchInvoicesByClient
        @ClientName VARCHAR(150)
    AS
    BEGIN
        SET NOCOUNT ON;
        SELECT * FROM invoices WHERE client_name LIKE '%' + @ClientName + '%';
    END
    """)


def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS sp_CreateInvoice")
    op.execute("DROP PROCEDURE IF EXISTS sp_GetInvoiceById")
    op.execute("DROP PROCEDURE IF EXISTS sp_SearchInvoicesByClient")
