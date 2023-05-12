"""Se hacen ajustes a los modelos para guardar las referencias de las imagenes

Revision ID: d30b7584ea32
Revises: 85bd6418d709
Create Date: 2023-05-11 19:08:36.303726

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd30b7584ea32'
down_revision = '85bd6418d709'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('foto_comentario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ruta_foto_comentario', sa.String(length=400), nullable=False))
        batch_op.drop_column('foto_comentario')

    with op.batch_alter_table('sitio', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['nombre_sitio'])

    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contrasena_hash', sa.String(length=128), nullable=True))
        batch_op.add_column(sa.Column('ruta_foto_usuario', sa.String(length=400), nullable=True))
        batch_op.create_unique_constraint(None, ['usuario'])
        batch_op.create_unique_constraint(None, ['correo_usuario'])
        batch_op.drop_column('contrasena')
        batch_op.drop_column('foto_usuario')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('foto_usuario', sa.BLOB(), nullable=True))
        batch_op.add_column(sa.Column('contrasena', mysql.VARCHAR(length=100), nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('ruta_foto_usuario')
        batch_op.drop_column('contrasena_hash')

    with op.batch_alter_table('sitio', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('foto_comentario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('foto_comentario', mysql.VARCHAR(length=400), nullable=False))
        batch_op.drop_column('ruta_foto_comentario')

    # ### end Alembic commands ###
