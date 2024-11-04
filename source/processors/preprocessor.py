import re
from typing import Dict, List, Tuple

class Preprocessor:
    @staticmethod
    def process_text(text: str) -> str:
        cleaned_text = (
            text.replace('&amp;amp;', '&')
            .replace('&amp;', '&')
            .replace('&lt;', '<')
            .replace('&gt;', '>')
            .replace('&quot;', '"')
            .replace('&apos;', "'")
        )

        cleaned_text = re.sub(r'<.*?>', '', cleaned_text)
        cleaned_text = cleaned_text.replace('\n', ' ').strip()
        for punct in ['.', ',', ':', ';', '!', '?']:
                cleaned_text = cleaned_text.replace(punct, f' {punct} ')
                cleaned_text = ' '.join(cleaned_text.split())

        return cleaned_text

    @staticmethod
    def process_sentiment(text: str) -> List[Tuple]:
        text = Preprocessor.process_text(text)
        triplets = tuple(map(lambda x: x.replace("EVAL_", "").split("_"), text.split(" ")))
        return triplets
