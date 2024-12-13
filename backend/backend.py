from laba4.data_management.data_management import DataManagement
from laba4.translator import QuoteTranslator


class Backend:
    def __init__(self):
        self.data_manager = DataManagement()
        self.translator = QuoteTranslator()
