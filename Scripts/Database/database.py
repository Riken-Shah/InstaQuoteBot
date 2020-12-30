import json
from Scripts.Helpers.common import send_request
import logging


class Database:
    """
    This class is basic template to integrate different databases.

    After integrating the custom db make sure to assign it in Scripts/__init__.py
    """

    def _check_quote_exist(self, quote):
        """
        Overwrite this function to check if the quote exist in db
        """

    def _add_quote(self, quote: str, author: str):
        """
        Overwrite this function to add quote in db
        """
        pass

    def add_single(self, quote: str, author: str):
        """
        Add single [quote, author] to the db
        """
        if not self._check_quote_exist(quote):
            self._add_quote(quote, author)
            return True
        return False

    def add_list(self, quotes: list, quote_key='quote', author_key='author'):
        """
        Add list of [quote, author] to the db
        """
        for quote in quotes:
            self.add_single(quote=quote[quote_key], author=quote[author_key])
        return True

    def fetch_quote(self):
        """
        Overwrite this function to return a [quote, author]
        """

    def is_empty(self):
        """
        Overwrite this function to return a boolean value to determine if db
        is empty or not
        """

    def add_from_api(self, quote_key='quote', author_key='author',  **kwargs):
        """
        Add data from APIs to the db
        """
        response = send_request(**kwargs)
        if str(response.status_code)[0] == '2':
            self.add_list(json.loads(response.content), author_key=author_key, quote_key=quote_key)
            logging.info(f'Data from {kwargs["url"]} is added successfully.')
        else:
            ConnectionError('API is not configured properly')
