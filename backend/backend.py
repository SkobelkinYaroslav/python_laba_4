from data_management.data_management import DataManagement
from translator import QuoteTranslator


class Backend:
    def __init__(self):
        self.data_manager = DataManagement()
        self.translator = QuoteTranslator()
