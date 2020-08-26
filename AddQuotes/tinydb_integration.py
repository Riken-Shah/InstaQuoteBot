from AddQuotes.add_quotes_from_api import AddFromApi
from Database.tinyDb import QuotesDatabase


class QuotesTinyDb(AddFromApi):
    def __init__(self, *args, **kwargs):
        self.db = QuotesDatabase()
        super().__init__(*args, **kwargs)

    def _write_to_db(self, quotes, quote_key, author_key):
        self.db.add_list(quotes, quote_key, author_key)
        return True
        
