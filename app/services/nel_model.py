from . import Embedder

class NELModel:
    _embedder_instance = Embedder()

    def __init__(self, session):
        self.embedder = NELModel._embedder_instance
        self.session = session
        
    def get_entity_embedding(self, entity):
        return self.embedder.get_embedding(entity)
