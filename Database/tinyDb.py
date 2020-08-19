from Database.database import Database
from tinydb import TinyDB, Query
from datetime import datetime
from secrets import tiny_db_path_to_db


class QuotesDatabase(TinyDB, Database):
    db_path = tiny_db_path_to_db

    def __init__(self, *args, **kwargs):
        super().__init__(self.db_path)
        self.query = Query()
        self.test_mode = kwargs['for_test'] or self.for_test

    # Check if quote exist
    def _check_quote_exist(self, quote):
        quotes = self.search(self.query.quote == quote)
        for _ in quotes:
            return True
        return False

    # Add [quote, author] to our db
    def _add_quote(self, quote: str, author: str):
        try:
            self.insert({'quote': quote, 'author': author, 'used_on_insta': False, 'timestamp': str(datetime.now())})
        except Exception as e:
            print(f'Error occurred while adding this quote -> {quote}, \n Error -> {e}')
            return False
        return True

    # Fetch the new quote
    def fetch_quote(self):
        """
        If no quotes are left in db it then it will return false
        :return quote or False:
        """
        quotes = self.search(self.query.used_on_insta == False)
        for quote in quotes:
            self.update({'used_on_insta': not self.test_mode}, doc_ids=[quote.doc_id])
            return {'quote': quote['quote'], 'author': quote['author']}
        return False
