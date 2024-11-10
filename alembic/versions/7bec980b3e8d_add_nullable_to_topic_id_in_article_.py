"""add nullable to topic_id in article_entity_sentiment_topics table

Revision ID: 7bec980b3e8d
Revises: f992dbcd1cc7
Create Date: 2024-11-08 18:43:24.568043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bec980b3e8d'
down_revision: Union[str, None] = 'f992dbcd1cc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article_entity_sentiment_topics', 'topic_id',
               existing_type=sa.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article_entity_sentiment_topics', 'topic_id',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###
