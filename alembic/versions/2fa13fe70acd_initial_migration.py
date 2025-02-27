"""Initial migration

Revision ID: 2fa13fe70acd
Revises: 
Create Date: 2024-11-02 00:29:24.091681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector

# revision identifiers, used by Alembic.
revision: str = '2fa13fe70acd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    op.create_table('articles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('apa_id', sa.String(), nullable=False),
    sa.Column('title_english', sa.String(), nullable=True),
    sa.Column('article_english', sa.Text(), nullable=True),
    sa.Column('title_german', sa.String(), nullable=True),
    sa.Column('article_german', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('entities',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('apa_id', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('source', sa.Enum('APA', 'NER', name='entity_source_enum'), nullable=False),
    sa.Column('type', sa.Enum('organization', 'person', 'product', name='entity_type_enum'), nullable=True),
    sa.Column('vector', pgvector.sqlalchemy.vector.VECTOR(dim=512), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('models',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('type', sa.Enum('NER', 'ABSA', 'TABSA', name='model_types_enum'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sentiments',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('apa_id', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('high', 'low', name='sentiment_type_enum'), nullable=True),
    sa.Column('vector', pgvector.sqlalchemy.vector.VECTOR(dim=512), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('topics',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('apa_id', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('individual', 'standard', name='topic_type_enum'), nullable=True),
    sa.Column('vector', pgvector.sqlalchemy.vector.VECTOR(dim=512), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article_entity_sentiment_aspects',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('article_id', sa.UUID(), nullable=False),
    sa.Column('entity_id', sa.UUID(), nullable=False),
    sa.Column('sentiment_id', sa.UUID(), nullable=False),
    sa.Column('topic_id', sa.String(), nullable=False),
    sa.Column('model_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['entity_id'], ['entities.id'], ),
    sa.ForeignKeyConstraint(['model_id'], ['models.id'], ),
    sa.ForeignKeyConstraint(['sentiment_id'], ['sentiments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('entity_mentions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('entity_id', sa.UUID(), nullable=False),
    sa.Column('article_id', sa.UUID(), nullable=False),
    sa.Column('start_pos', sa.Integer(), nullable=False),
    sa.Column('end_pos', sa.Integer(), nullable=False),
    sa.Column('confidence', sa.Integer(), nullable=True),
    sa.Column('source', sa.Enum('APA', 'NER', name='entity_mention_source_enum'), nullable=False),
    sa.Column('type', sa.Enum('ORG', 'PER', 'LOC', 'MISC', name='entity_mention_type_enum'), nullable=False),
    sa.Column('vector', pgvector.sqlalchemy.vector.VECTOR(dim=512), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['entity_id'], ['entities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entity_mentions')
    op.drop_table('article_entity_sentiment_aspects')
    op.drop_table('topics')
    op.drop_table('sentiments')
    op.drop_table('models')
    op.drop_table('entities')
    op.drop_table('articles')
    # ### end Alembic commands ###
