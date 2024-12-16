import requests

class Quote:
    def __init__(self, text: str, author: str):
        self._text = text
        self._author = author

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    def __str__(self):
        return f'"{self.text}" - {self.author}'

