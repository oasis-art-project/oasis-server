"""empty message

Revision ID: 3510860323b7
Revises: 
Create Date: 2021-09-06 13:35:21.365533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3510860323b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('files', sa.String(length=1000), nullable=True),
    sa.Column('tags', sa.String(length=100), nullable=True),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('token_type', sa.String(length=10), nullable=False),
    sa.Column('user_identity', sa.Integer(), nullable=False),
    sa.Column('revoked', sa.Boolean(), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('files', sa.String(length=1000), nullable=True),
    sa.Column('tags', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('firstName', sa.String(length=50), nullable=False),
    sa.Column('lastName', sa.String(length=50), nullable=True),
    sa.Column('bio', sa.String(length=2000), nullable=True),
    sa.Column('role', sa.Integer(), nullable=False),
    sa.Column('homepage', sa.String(length=100), nullable=True),
    sa.Column('instagram', sa.String(length=30), nullable=True),
    sa.Column('youtube', sa.String(length=30), nullable=True),
    sa.Column('phone', sa.String(length=10), nullable=True),
    sa.Column('showChat', sa.Boolean(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('creation_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('artworks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('files', sa.String(length=1000), nullable=True),
    sa.Column('tags', sa.String(length=100), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.Column('medium', sa.String(length=200), nullable=True),
    sa.Column('size', sa.String(length=200), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('link', sa.String(length=100), nullable=True),
    sa.Column('creation_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('files', sa.String(length=1000), nullable=True),
    sa.Column('tags', sa.String(length=100), nullable=True),
    sa.Column('host_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.Column('address', sa.String(length=300), nullable=False),
    sa.Column('location', sa.String(length=12), nullable=True),
    sa.Column('homepage', sa.String(length=100), nullable=True),
    sa.Column('instagram', sa.String(length=30), nullable=True),
    sa.Column('facebook', sa.String(length=30), nullable=True),
    sa.Column('matterport_link', sa.String(length=15), nullable=True),
    sa.Column('creation_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['host_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('files', sa.String(length=1000), nullable=True),
    sa.Column('tags', sa.String(length=100), nullable=True),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.Column('link', sa.String(length=100), nullable=True),
    sa.Column('hubs_link', sa.String(length=10), nullable=True),
    sa.Column('startTime', sa.DateTime(), nullable=False),
    sa.Column('endTime', sa.DateTime(), nullable=True),
    sa.Column('creation_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('artists_association',
    sa.Column('artist', sa.Integer(), nullable=True),
    sa.Column('event', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist'], ['users.id'], ),
    sa.ForeignKeyConstraint(['event'], ['events.id'], )
    )
    op.create_table('artworks_association',
    sa.Column('artwork', sa.Integer(), nullable=True),
    sa.Column('event', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artwork'], ['artworks.id'], ),
    sa.ForeignKeyConstraint(['event'], ['events.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artworks_association')
    op.drop_table('artists_association')
    op.drop_table('events')
    op.drop_table('places')
    op.drop_table('artworks')
    op.drop_table('users')
    op.drop_table('tokens')
    # ### end Alembic commands ###
