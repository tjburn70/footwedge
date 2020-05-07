"""init models

Revision ID: 3b7c795f3f4f
Revises: 
Create Date: 2020-05-07 10:35:46.035205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b7c795f3f4f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'golf_club',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=True),
        sa.Column('state_code', sa.String(), nullable=True),
        sa.Column('county', sa.String(), nullable=True),
        sa.Column('zip_code', sa.String(), nullable=True),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('created_ts', sa.DateTime(), nullable=False),
        sa.Column('touched_ts', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )

    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('middle_initial', sa.String(), nullable=True),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('created_ts', sa.DateTime(), nullable=False),
        sa.Column('touched_ts', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )

    op.create_index(op.f('ix_public_user_email'), 'user', ['email'], unique=True, schema='public')

    op.create_table(
        'golf_course',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('golf_club_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('num_holes', sa.Integer(), nullable=True),
        sa.Column('created_ts', sa.DateTime(), nullable=False),
        sa.Column('touched_ts', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['golf_club_id'], ['public.golf_club.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )

    op.create_table(
        'handicap',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('index', sa.Numeric(), nullable=False),
        sa.Column('authorized_association', sa.String(), nullable=True),
        sa.Column('record_start_date', sa.DateTime(), nullable=False),
        sa.Column('record_end_date', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['public.user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )

    op.create_table(
        'profile',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('home_course', sa.String(), nullable=True),
        sa.Column('dexterity', sa.String(), nullable=True),
        sa.Column('created_ts', sa.DateTime(), nullable=False),
        sa.Column('touched_ts', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['public.user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )

    op.create_table(
        'tee_box',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('golf_course_id', sa.Integer(), nullable=False),
        sa.Column('tee_color', sa.String(), nullable=True),
        sa.Column('par', sa.Integer(), nullable=False),
        sa.Column('distance', sa.Integer(), nullable=False),
        sa.Column('unit', sa.String(), nullable=False),
        sa.Column('course_rating', sa.Numeric(), nullable=False),
        sa.Column('slope', sa.Numeric(), nullable=False),
        sa.Column('created_ts', sa.DateTime(), nullable=False),
        sa.Column('touched_ts', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['golf_course_id'], ['public.golf_course.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )

    op.create_table(
        'golf_round',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('golf_course_id', sa.Integer(), nullable=False),
        sa.Column('tee_box_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('gross_score', sa.Integer(), nullable=False),
        sa.Column('towards_handicap', sa.Boolean(), nullable=False),
        sa.Column('played_on', sa.Date(), nullable=False),
        sa.Column('created_ts', sa.DateTime(), nullable=False),
        sa.Column('touched_ts', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['golf_course_id'], ['public.golf_course.id'], ),
        sa.ForeignKeyConstraint(['tee_box_id'], ['public.tee_box.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['public.user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )

    op.create_table(
        'hole',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('golf_course_id', sa.Integer(), nullable=False),
        sa.Column('tee_box_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('hole_number', sa.Integer(), nullable=False),
        sa.Column('par', sa.Integer(), nullable=False),
        sa.Column('handicap', sa.Integer(), nullable=False),
        sa.Column('distance', sa.Integer(), nullable=False),
        sa.Column('unit', sa.String(), nullable=False),
        sa.Column('created_ts', sa.DateTime(), nullable=False),
        sa.Column('touched_ts', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['golf_course_id'], ['public.golf_course.id'], ),
        sa.ForeignKeyConstraint(['tee_box_id'], ['public.tee_box.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )

    op.create_table(
        'golf_round_stats',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('golf_round_id', sa.Integer(), nullable=False),
        sa.Column('hole_id', sa.Integer(), nullable=False),
        sa.Column('gross_score', sa.Integer(), nullable=False),
        sa.Column('fairway_hit', sa.Boolean(), nullable=True),
        sa.Column('green_in_regulation', sa.Boolean(), nullable=False),
        sa.Column('putts', sa.Integer(), nullable=False),
        sa.Column('chips', sa.Integer(), nullable=False),
        sa.Column('greenside_sand_shots', sa.Integer(), nullable=False),
        sa.Column('penalties', sa.Integer(), nullable=False),
        sa.Column('created_ts', sa.DateTime(), nullable=False),
        sa.Column('touched_ts', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['golf_round_id'], ['public.golf_round.id'], ),
        sa.ForeignKeyConstraint(['hole_id'], ['public.hole.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='public'
    )


def downgrade():
    op.drop_table('golf_round_stats', schema='public')
    op.drop_table('hole', schema='public')
    op.drop_table('golf_round', schema='public')
    op.drop_table('tee_box', schema='public')
    op.drop_table('profile', schema='public')
    op.drop_table('handicap', schema='public')
    op.drop_table('golf_course', schema='public')
    op.drop_index(op.f('ix_public_user_email'), table_name='user', schema='public')
    op.drop_table('user', schema='public')
    op.drop_table('golf_club', schema='public')
