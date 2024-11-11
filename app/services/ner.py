from flair.data import Sentence
from flair.models import SequenceTagger

class NER:
    def __init__(self, tagger):
        self.tagger = tagger
        self.accepted_entity_types = ['PER', 'ORG']

    def get_sentences_from_article(self, article):
        sentences = []
        for sentence in article.split('.'):
            sentences.append(sentence + '.')
        return sentences

    def get_named_entities(self, article):
        length = 0
        sentences = self.get_sentences_from_article(article)
        named_entities = []
        for sentence in sentences:
            s = Sentence(sentence)
            self.tagger.predict(s)
            for entity in s.get_spans('ner'):
                named_entities.append(
                    self.prepare_entity(
                        entity=entity, 
                        start_pos = int(entity.start_position) + length, 
                        end_pos = int(entity.end_position) + length
                    )
                )
            length += len(sentence)

        return self.filter_entities(named_entities)
    
    def filter_entities(self, entities):
        return list(filter(lambda x: x["type"] in self.accepted_entity_types, entities))
    
    def prepare_entity(self, entity, start_pos, end_pos):
        return {
            "name": entity.text,
            "type": entity.get_label("ner").value,
            "confidence": entity.get_label("ner").score,
            "start_pos": start_pos,
            "end_pos": end_pos
        }
