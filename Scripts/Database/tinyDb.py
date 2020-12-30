from Scripts.Database.database import Database
from tinydb import TinyDB, Query
from datetime import datetime
import os
import logging


class QuotesDatabase(Database):
    def __init__(self, *args, **kwargs):
        super().__init__()
        db_path = 'quotes_database.json'
        if not os.path.exists(db_path):
            # Create file if not present
            logging.warning('No database file detected.')
            open(db_path, 'w')
            logging.info('Creating new database file.')
        self.db = TinyDB(db_path)
        self.query = Query()

    def _check_quote_exist(self, quote):
        return bool(self.db.search(self.query.quote == quote))

    def _add_quote(self, quote: str, author: str):
        try:
            self.db.insert({'quote': quote, 'author': author, 'used_on_insta': False, 'timestamp': str(datetime.now())})
        except Exception as e:
            logging.error(f'Error occurred while adding quote -> {quote}, \n Error -> {e}')
            return False
        return True

    def fetch_quote(self):
        """
        If no quotes are left in db it then it will return random quote
        :return [quote, author] dict
        """
        quotes = self.db.search(self.query.used_on_insta == False)
        if not quotes:
            quotes = self.db.search(self.query.used_on_insta == True)
        quote = quotes[0]
        self.db.update({'used_on_insta': True}, doc_ids=[quote.doc_id])
        return {'quote': quote['quote'], 'author': quote['author']}

    def is_empty(self):
        return len(self.db.all()) == 0
