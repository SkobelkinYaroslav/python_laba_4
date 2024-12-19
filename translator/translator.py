from googletrans import Translator
from ..models import Quote


class QuoteTranslator:
    def __init__(self):
        self.translator = Translator()

    def translate(self, quote: Quote) -> Quote:
        translated_text = self.translator.translate(quote.text, dest='ru')
        translated_author = self.translator.translate(quote.author, dest='ru')

        return Quote(
            translated_text.text,
            translated_author.text,
        )

