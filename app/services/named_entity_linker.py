import numpy as np

from numpy.linalg import norm
from rapidfuzz import fuzz
from typing import List


class NamedEntityLinker:
    def get_most_similar_embedding(self, vector: List, matrix: List[List]):
        similarities = np.dot(matrix, vector) / (norm(matrix, axis=1) * norm(vector))
        most_similar_idx = np.argmax(similarities)
        return similarities[most_similar_idx], most_similar_idx

    def get_most_similar_name(self, name: str, entity_names: List[str]):
        similarities = [fuzz.partial_ratio(name, entity_name) for entity_name in entity_names]
        most_similar_idx = np.argmax(similarities)
        return similarities[most_similar_idx]*0.01, most_similar_idx

    def get_most_similar_entity(self, vector, matrix, name, entity_names):
        embed_similarity, embed_entity_idx = self.get_most_similar_embedding(vector, matrix)
        name_similarity, name_entity_idx = self.get_most_similar_name(name, entity_names)
        return  max(embed_similarity, name_similarity), embed_entity_idx if embed_similarity > name_similarity else name_entity_idx
    