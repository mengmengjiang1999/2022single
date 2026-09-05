"""Initial migration

Revision ID: 8bb29312a83b
Revises: 
Create Date: 2022-05-08 21:44:14.947960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bb29312a83b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'userinfo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=True),
        sa.Column('password', sa.String(length=256), nullable=True),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('submitted', sa.Integer(), nullable=False),
        sa.Column('correct', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )
    op.create_table(
        'problem',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=True),
        sa.Column('problem_id', sa.String(length=120), nullable=False),
        sa.Column('problem_type', sa.Integer(), nullable=False),
        sa.Column('status', sa.Integer(), nullable=False),
        sa.Column('problem_time', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('problem_id'),
    )
    op.create_table(
        'course',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('coursename', sa.String(length=80), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('status', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'coursename', 'username', name='uq_course_member'
        ),
    )
    op.create_table(
        'course_homework',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('courseid', sa.Integer(), nullable=False),
        sa.Column('homework', sa.Integer(), nullable=True),
        sa.Column('starttime', sa.Integer(), nullable=False),
        sa.Column('endtime', sa.Integer(), nullable=False),
        sa.Column('count', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('course_homework')
    op.drop_table('course')
    op.drop_table('problem')
    op.drop_table('userinfo')
