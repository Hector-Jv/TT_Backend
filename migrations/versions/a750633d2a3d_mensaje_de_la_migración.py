"""mensaje de la migración

Revision ID: a750633d2a3d
Revises: 6ad7831d1da1
Create Date: 2023-06-27 03:27:58.119351

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a750633d2a3d'
down_revision = '6ad7831d1da1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comentario', schema=None) as batch_op:
        batch_op.alter_column('calificacion',
               existing_type=mysql.INTEGER(),
               type_=sa.Float(precision=5),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comentario', schema=None) as batch_op:
        batch_op.alter_column('calificacion',
               existing_type=sa.Float(precision=5),
               type_=mysql.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
