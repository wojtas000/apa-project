from fastapi import FastAPI
from sqladmin import Admin, ModelView
from app.database import sessionmanager
from app.models import Article, Entity, EntityMention, Topic, Sentiment, ArticleEntitySentimentTopic, Model


class ArticleAdmin(ModelView, model=Article):
    column_list = [Article.id, Article.apa_id, Article.title, Article.language, Article.article, Article.created_at, Article.updated_at]
    column_searchable_list = [Article.id, Article.title, Article.apa_id]
    name = "Article"
    name_plural = "Articles"


class EntityAdmin(ModelView, model=Entity):
    column_list = [Entity.id, Entity.apa_id, Entity.name, Entity.source, Entity.type, Entity.created_at, Entity.updated_at]
    column_searchable_list = [Entity.id, Entity.name, Entity.apa_id]
    name = "Entity"
    name_plural = "Entities"


class EntityMentionAdmin(ModelView, model=EntityMention):
    column_list = [EntityMention.id, EntityMention.entity_id, EntityMention.article_id, EntityMention.start_pos, EntityMention.end_pos, EntityMention.confidence, EntityMention.source, EntityMention.type, EntityMention.created_at, EntityMention.updated_at]
    column_searchable_list = [EntityMention.id, EntityMention.source, EntityMention.type]
    name = "Entity Mention"
    name_plural = "Entity Mentions"


class TopicAdmin(ModelView, model=Topic):
    column_list = [Topic.id, Topic.apa_id, Topic.name, Topic.type, Topic.created_at, Topic.updated_at]
    column_searchable_list = [Topic.id, Topic.name, Topic.apa_id]
    name = "Topic"
    name_plural = "Topics"


class SentimentAdmin(ModelView, model=Sentiment):
    column_list = [Sentiment.id, Sentiment.apa_id, Sentiment.name, Sentiment.type, Sentiment.created_at, Sentiment.updated_at]
    column_searchable_list = [Sentiment.id, Sentiment.name, Sentiment.apa_id]
    name = "Sentiment"
    name_plural = "Sentiments"


class ArticleEntitySentimentTopicAdmin(ModelView, model=ArticleEntitySentimentTopic):
    column_list = [ArticleEntitySentimentTopic.id, ArticleEntitySentimentTopic.article_id, ArticleEntitySentimentTopic.entity_id, ArticleEntitySentimentTopic.sentiment_id, ArticleEntitySentimentTopic.topic_id, ArticleEntitySentimentTopic.created_at, ArticleEntitySentimentTopic.updated_at]
    column_searchable_list = [ArticleEntitySentimentTopic.article_id, ArticleEntitySentimentTopic.entity_id, ArticleEntitySentimentTopic.sentiment_id, ArticleEntitySentimentTopic.topic_id]
    name = "Article Entity Sentiment Topic"
    name_plural = "Article Entity Sentiment Topics"


class ModelAdmin(ModelView, model=Model):
    column_list = [Model.id, Model.name, Model.type, Model.created_at, Model.updated_at]
    column_searchable_list = [Model.id, Model.name]
    name = "Model"
    name_plural = "Models"


def init_admin(app: FastAPI):
    admin = Admin(app, engine=sessionmanager._engine)
    admin.add_view(ArticleAdmin)
    admin.add_view(EntityAdmin)
    admin.add_view(EntityMentionAdmin)
    admin.add_view(TopicAdmin)
    admin.add_view(SentimentAdmin)
    admin.add_view(ArticleEntitySentimentTopicAdmin)
    admin.add_view(ModelAdmin)

