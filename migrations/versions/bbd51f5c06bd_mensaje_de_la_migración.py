"""mensaje de la migración

Revision ID: bbd51f5c06bd
Revises: ead6052b16a0
Create Date: 2023-05-19 20:50:25.986801

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bbd51f5c06bd'
down_revision = 'ead6052b16a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('etiqueta_tipo_sitio')
    with op.batch_alter_table('foto_sitio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nombre_imagen', sa.String(length=300), nullable=False))

    with op.batch_alter_table('tipo_sitio', schema=None) as batch_op:
        batch_op.drop_column('ruta_imagen')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tipo_sitio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ruta_imagen', mysql.VARCHAR(length=400), nullable=True))

    with op.batch_alter_table('foto_sitio', schema=None) as batch_op:
        batch_op.drop_column('nombre_imagen')

    op.create_table('etiqueta_tipo_sitio',
    sa.Column('cve_tipo_sitio', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('cve_etiqueta', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['cve_etiqueta'], ['etiqueta.cve_etiqueta'], name='etiqueta_tipo_sitio_ibfk_1'),
    sa.ForeignKeyConstraint(['cve_tipo_sitio'], ['tipo_sitio.cve_tipo_sitio'], name='etiqueta_tipo_sitio_ibfk_2'),
    sa.PrimaryKeyConstraint('cve_tipo_sitio', 'cve_etiqueta'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
