from deep_translator import GoogleTranslator
from models import Quote

class QuoteTranslator:
    @staticmethod
    def translate(quote: Quote) -> Quote:
        """

        :param quote: Цитата для перевода
        :return: Новая переведенная цитата
        """
        translated_text = GoogleTranslator(source='auto', target='ru').translate(quote.text)
        translated_author = GoogleTranslator(source='auto', target='ru').translate(quote.author)

        return Quote(
            translated_text,
            translated_author,
        )