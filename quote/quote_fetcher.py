import requests


class RandomQuoteFetcher:
    @staticmethod
    def get_random_quote():
        """
        Получает случайную цитату из API.
        :return: строка с цитатой или сообщение об ошибке.
        """
        try:
            response = requests.get("https://zenquotes.io/api/random")
            response.raise_for_status()  # Генерирует исключение, если статус ответа не 200
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Ошибка при обращении к API: {e}"