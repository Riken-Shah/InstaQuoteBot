class Database:
    """
    This class is basic template to integrate with the diffrent
    Database
    """

    # Check if quote exist
    def __check_quote_exist(self, quote):
        """
        Overwrite this function to return if the quote exist in db
        """

    # Add [quote, author] to our db
    def __add_quote(self, quote: str, author: str):
        """
        Overwrite this function to add quote in db
        """
        pass

    # Add single quote
    def add_single(self, quote: str, author: str):
        if not self.__check_quote_exist(quote):
            self.__add_quote(quote, author)
            return True
        return False

    # Add list of quotes
    def add_list(self, quotes: list, quote_key='quote', author_key='author'):
        for quote in quotes:
            self.add_single(quote=quote[quote_key], author=quote[author_key])
        return True

    # Fetch Quote and Author from db
    def fetch_quote(self, for_test=False):
        """
        Overwrite this function to return a quote and the update it used_on_insta = True
        """
