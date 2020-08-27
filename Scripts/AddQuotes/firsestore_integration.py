from Scripts.AddQuotes.add_quotes_from_api import AddFromApi
from Scripts.Database.firestore import QuotesDatabase


class FireStoreIntegration(AddFromApi):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Give your path to Firebase Admin SDK Cred
        self.db = QuotesDatabase('../intagram-bot-firebase-adminsdk-slaoe-3e8bc1ca0a.json')

    def __write_to_db(self, quotes, quote_key, author_key):
        """
        This function writes a list of quotes to our db
        """
        self.db.add_list(quotes, quote_key, author_key)
        return True


