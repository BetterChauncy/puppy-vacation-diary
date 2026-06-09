"""add likes_count and comments table

Revision ID: 1a2b3c4d5e6f
Revises: 8cceb6680e64
Create Date: 2026-06-09 14:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a2b3c4d5e6f'
down_revision: Union[str, Sequence[str], None] = '8cceb6680e64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('media', sa.Column('likes_count', sa.Integer(), nullable=False, server_default='0'))
    op.create_table('comments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('media_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['media_id'], ['media.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_media_id'), 'comments', ['media_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_comments_media_id'), table_name='comments')
    op.drop_table('comments')
    op.drop_column('media', 'likes_count')
