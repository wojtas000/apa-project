"""Add nullable to model_id in article_entity_sentiment_topics table

Revision ID: f992dbcd1cc7
Revises: 329ca6aec6df
Create Date: 2024-11-08 18:30:42.977795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f992dbcd1cc7'
down_revision: Union[str, None] = '329ca6aec6df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article_entity_sentiment_topics', 'model_id',
               existing_type=sa.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article_entity_sentiment_topics', 'model_id',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###
