"""mensaje de la migración

Revision ID: b6f657ba38ff
Revises: e3c018ccb8cc
Create Date: 2023-06-05 15:35:42.074535

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b6f657ba38ff'
down_revision = 'e3c018ccb8cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('foto_sitio', schema=None) as batch_op:
        batch_op.alter_column('nombre_autor',
               existing_type=mysql.VARCHAR(length=400),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('foto_sitio', schema=None) as batch_op:
        batch_op.alter_column('nombre_autor',
               existing_type=mysql.VARCHAR(length=400),
               nullable=True)

    # ### end Alembic commands ###
