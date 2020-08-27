from Scripts.Database.database import Database
from tinydb import TinyDB, Query
from datetime import datetime
import os


class QuotesDatabase(Database):
    def __init__(self, *args, **kwargs):
        db_path = os.getenv('tiny_db_path_to_db')
        if not db_path:
            raise ValueError('DB path not found')
        self.db = TinyDB(db_path)
        # super().__init__(self.db_path)
        self.query = Query()
        if 'for_test' in kwargs:
            self.test_mode = kwargs['for_test']
        else:
            self.test_mode = False

    # Check if quote exist
    def _check_quote_exist(self, quote):
        """
        Check is some quote exists
        """
        quotes = self.db.search(self.query.quote == quote)
        for _ in quotes:
            return True
        return False

    # Add [quote, author] to our db
    def _add_quote(self, quote: str, author: str):
        """
        Add single quote to the db
        """

        try:
            self.db.insert({'quote': quote, 'author': author, 'used_on_insta': False, 'timestamp': str(datetime.now())})
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
        quotes = self.db.search(self.query.used_on_insta == False)
        for quote in quotes:
            self.db.update({'used_on_insta': not self.test_mode}, doc_ids=[quote.doc_id])
            return {'quote': quote['quote'], 'author': quote['author']}
        return False
