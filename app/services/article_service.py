import re

from sqlalchemy.ext.asyncio import AsyncSession
from collections import defaultdict
from typing import List

from app.repositories import ArticleRepository


class ArticleService:
    def __init__(self, db: AsyncSession):
        self.repository = ArticleRepository(db)

    def split_into_sentences(self, text: str) -> List[str]:
        sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
        return sentence_endings.split(text)


    def get_closest_sentences(self, sentences: List[str], mention_pos: List[int]) -> List[str]:
        closest_sentences = []
        for pos in mention_pos:
            if pos > 0:
                closest_sentences.append(sentences[pos - 1])
            closest_sentences.append(sentences[pos])
            if pos < len(sentences) - 1:
                closest_sentences.append(sentences[pos + 1])
        return closest_sentences


    def deduplicate_and_format(self, mention_sentences: List[str]) -> str:
        return '...'.join(list(dict.fromkeys(mention_sentences)))


    def get_training_data_for_entity(self, mentions, article_text) -> List[dict]:
        sentences = self.split_into_sentences(article_text)
        mention_sentences = []

        for mention in mentions:
            mention_pos = [i for i, sentence in enumerate(sentences) if mention["mention"] in sentence]
            closest_sentences = self.get_closest_sentences(sentences, mention_pos)
            mention_sentences.extend(closest_sentences)

        shortened_text = self.deduplicate_and_format(mention_sentences)
        for mention in mentions:
            shortened_text = shortened_text.replace(mention["mention"], "$T$")
        return {
            "entity_name": mentions[0]["entity_name"],
            "sentiment": mentions[0]["sentiment"],
            "text": shortened_text
        }


    async def get_training_data(self, article_id: str, with_ambivalent: bool = False) -> dict:
        rows = await self.repository.get_training_data(article_id)
        if not rows:
            return {"training_data": []}

        mentions_by_entity = defaultdict(list)
        for row in rows:
            mentions_by_entity[row.entity_id].append({
                "entity_name": row.entity_name,
                "mention": row.name,
                "sentiment": row.sentiment_name.capitalize()
            })
        article_text = row.article_text

        entity_mentions = []
        for entity_name, mentions in mentions_by_entity.items():
            entity_mentions.append(self.get_training_data_for_entity(mentions, article_text))

        return {"training_data": entity_mentions}