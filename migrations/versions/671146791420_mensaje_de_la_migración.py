"""mensaje de la migración

Revision ID: 671146791420
Revises: 64aa29b8b06a
Create Date: 2023-06-11 14:27:21.914008

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '671146791420'
down_revision = '64aa29b8b06a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comentario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('calificacion', sa.Integer(), nullable=True))
        batch_op.alter_column('comentario',
               existing_type=mysql.VARCHAR(length=400),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comentario', schema=None) as batch_op:
        batch_op.alter_column('comentario',
               existing_type=mysql.VARCHAR(length=400),
               nullable=False)
        batch_op.drop_column('calificacion')

    # ### end Alembic commands ###
