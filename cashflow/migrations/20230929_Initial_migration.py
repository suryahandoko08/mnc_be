from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abcdef123456'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create User table
    op.create_table(
        'user',
        sa.Column('id', sa.String(), primary_key=True, nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('phone_number', sa.String(), unique=True, nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('pin', sa.String(), nullable=False),
        sa.Column('balance', sa.Integer(), default=0),
        sa.Column('created_date', sa.DateTime(), default=sa.func.now())
    )
    
    # Create Transaction table
    op.create_table(
        'transaction',
        sa.Column('id', sa.String(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.String(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('remarks', sa.String(), nullable=True),
        sa.Column('transaction_type', sa.String(), nullable=False),
        sa.Column('created_date', sa.DateTime(), default=sa.func.now())
    )


def downgrade():
    op.drop_table('transaction')
    op.drop_table('user')
