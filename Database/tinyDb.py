from Database.database import Database
from tinydb import TinyDB, Query
from datetime import datetime


class QuotesDatabase(TinyDB, Database):
    def __init__(self, filename=None, *args, **kwargs):
        super().__init__(filename or 'quotes_data.json', *args, **kwargs)
        self.query = Query()

    # Check if quote exist
    def __check_quote_exist(self, quote):
        quotes = self.search(self.query.quote == quote)
        for _ in quotes:
            return True
        return False

    # Add [quote, author] to our db
    def __add_quote(self, quote: str, author: str):
        try:
            self.insert({'quote': quote, 'author': author, 'used_on_insta': False, 'timestamp': str(datetime.now())})
        except Exception as e:
            print(f'Error occurred while adding this quote -> {quote}, \n Error -> {e}')
            return False
        return True

    # Fetch the new quote
    def fetch_quote(self, for_test=False):
        """
        If no quotes are left in db it then it will return false
        :return quote or False:
        """
        quotes = self.search(self.query.used_on_insta == False)
        for quote in quotes:
            self.update({'used_on_insta': not for_test}, doc_ids=[quote.doc_id])
            return {'quote': quote['quote'], 'author': quote['author']}
        return False

