from sqladmin import Admin, ModelView
from app.models import Conversation, Document, Page, Block, AdverseMedium, ChatHistory, AdverseMediaStatus
from app.database import sessionmanager
from fastapi import FastAPI
from wtforms.fields import SelectField


class ConversationAdmin(ModelView, model=Conversation):
    column_list = [Conversation.id, Conversation.name, Conversation.created_at, Conversation.is_active]
    column_searchable_list = [Conversation.name]
    name = "Conversation"
    name_plural = "Conversations"

class DocumentAdmin(ModelView, model=Document):
    column_list = [Document.id, Document.name, Document.language, Document.created_at]
    column_searchable_list = [Document.name]
    name = "Document"
    name_plural = "Documents"

def init_admin(app: FastAPI):
    admin = Admin(app, engine=sessionmanager._engine)
    admin.add_view(ConversationAdmin)
    admin.add_view(DocumentAdmin)
