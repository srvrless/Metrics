"""nevers

Revision ID: f1135d1439d7
Revises: 
Create Date: 2023-04-02 12:40:45.695977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1135d1439d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('capitalizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total_purchase', sa.Integer(), nullable=False),
    sa.Column('company_inn', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'purchases', type_='unique')
    op.alter_column('purchases', 'customer_inn',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.alter_column('participants', 'supplier_inn',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.add_column('contracts', sa.Column('contract_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'companies', type_='unique')
    op.drop_constraint(None, 'companies', type_='unique')
    op.drop_constraint(None, 'companies', type_='unique')
    op.drop_constraint(None, 'companies', type_='unique')
    op.alter_column('companies', 'supplier_inn',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.alter_column('companies', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    op.drop_table('capitalizations')
    # ### end Alembic commands ###