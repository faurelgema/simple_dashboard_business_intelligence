"""dataset table only

Revision ID: 15c6ad84a800
Revises: 
Create Date: 2022-06-15 10:36:53.083666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15c6ad84a800'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dataset',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('judul', sa.String(length=255), nullable=False),
    sa.Column('deskripsi', sa.Text(), nullable=True),
    sa.Column('tahun', sa.Integer(), nullable=False),
    sa.Column('topik', sa.String(length=255), nullable=False),
    sa.Column('organisasi', sa.String(length=255), nullable=False),
    sa.Column('cuid', sa.Integer(), nullable=False),
    sa.Column('muid', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=230), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('role', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('dataset')
    # ### end Alembic commands ###
