import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime


class QuotesDatabase:
    """
    This class manages our quote database
    It provides following methods:
    -> ADD
    -> FETCH
    """

    def __init__(self, path_to_certificate):
        """
        Connecting to Firebase
        """
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate(path_to_certificate)

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred)

        # Getting quotes instance
        self.db = firestore.client().collection(u'quotes')

    # Check if quote exist
    def __check_quote_exist(self, quote):
        try:
            quotes = self.db.where(u'quote', u'==', quote).stream()
        except Exception as e:
            print(f'Error occurred while checking this quote -> {quote}, \n Error -> {e}')
            return False
        for _ in quotes:
            return True
        return False

    # Add [quote, author] to our db
    def __add_quote(self, quote: str, author: str):
        try:
            self.db.document().set({'quote': quote, 'author': author, 'used_on_insta': False, 'timestamp': datetime.now()})
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
        quotes = self.db.where(u'used_on_insta', u'==', False).stream()
        for quote in quotes:
            self.db.document(quote.id).update({u'used_on_insta': not for_test})
            quote = quote.to_dict()
            return {'quote': quote['quote'], 'author': quote['author']}
        return False




