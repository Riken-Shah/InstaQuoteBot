from Scripts.AddQuotes.add_quotes_from_api import AddFromApi
from Scripts.Database.tinyDb import QuotesDatabase


class QuotesTinyDb(AddFromApi):
    def __init__(self, *args, **kwargs):
        self.db = QuotesDatabase()
        super().__init__(*args, **kwargs)

    def _write_to_db(self, quotes, quote_key, author_key):
        """
        This function writes a list of quotes to our db
        """
        self.db.add_list(quotes, quote_key, author_key)
        return True
        
