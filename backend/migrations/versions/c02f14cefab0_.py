"""empty message

Revision ID: c02f14cefab0
Revises: 6a253ec7f891
Create Date: 2018-09-15 18:52:15.177015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c02f14cefab0'
down_revision = '6a253ec7f891'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('ip', sa.String(length=40), nullable=True),
    sa.Column('os', sa.String(length=50), nullable=True),
    sa.Column('browser', sa.String(length=100), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('expired_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_session_token'), 'session', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_session_token'), table_name='session')
    op.drop_table('session')
    # ### end Alembic commands ###
