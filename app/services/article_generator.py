from typing import Generator, Dict
import xml.etree.ElementTree as ET

class ArticleGenerator:
    @staticmethod
    def generate_articles(data) -> Generator[Dict[str, str], None, None]:
        root = ET.fromstring(data)
        
        for document in root.findall('.//Document'):
            doc_id = document.get('id')
            published_date = document.find('.//DOC').get('TIMESTAMP')
            title = document.find(".//FELD[@NAME='TITEL']")
            article = document.find(".//FELD[@NAME='INHALT']")
            sentiments = document.find(".//FELD[@NAME='EVALUATIONS']")
            try:
                yield {
                    "apa_id": doc_id,
                    "published_date": published_date,
                    "title": ET.tostring(title, encoding='unicode', method='text'),
                    "article": ET.tostring(article, encoding='unicode', method='text'),
                    "sentiments": ET.tostring(sentiments, encoding='unicode', method='text'),
                }
            except:
                continue
