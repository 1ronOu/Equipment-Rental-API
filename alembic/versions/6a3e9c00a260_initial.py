from alembic import op
import sqlalchemy as sa

revision = '6a3e9c00a260'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=30), nullable=True),
        sa.Column('price', sa.Integer, nullable=True),
        sa.Column('description', sa.String(length=30), nullable=True),  
    )

def downgrade() -> None:
    op.drop_table('products')
