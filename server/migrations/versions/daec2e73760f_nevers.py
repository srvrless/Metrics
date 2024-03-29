"""nevers

Revision ID: daec2e73760f
Revises: a58aa439b140
Create Date: 2023-04-01 09:09:05.126105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daec2e73760f'
down_revision = 'a58aa439b140'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('participants_supplier_inn_key', 'participants', type_='unique')
    op.create_foreign_key(None, 'participants', 'companies', ['supplier_inn'], ['supplier_inn'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'participants', type_='foreignkey')
    op.create_unique_constraint('participants_supplier_inn_key', 'participants', ['supplier_inn'])
    # ### end Alembic commands ###
