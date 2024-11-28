import re
from typing import List, Tuple
from datetime import datetime

class Preprocessor:
    def process_text(self, text: str) -> str:
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
        cleaned_text = self.fix_punctuation(cleaned_text)

        return cleaned_text

    def fix_punctuation(self, text: str) -> str:
        for punct in ['.', ',', ':', ';', '!', '?']:
            text = text.replace(punct, f' {punct} ')
            text = ' '.join(text.split())
        return text

    def process_sentiment(self, text: str) -> List[Tuple]:
        text = self.process_text(text)
        triplets = tuple(map(lambda x: x.replace("EVAL_", "").split("_"), text.split(" ")))
        return triplets

    def fix_date(self, date_string: str) -> str:
        date_format = "%Y-%m-%d %H:%M:%S"
        return datetime.strptime(date_string, date_format)
