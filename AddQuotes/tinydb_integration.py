from AddQuotes.add_quotes_from_api import AddFromApi
from datetime import datetime
from tinydb import TinyDB
from Database.tinyDb import QuotesDatabase


class QuotesTinyDb(AddFromApi):
    def __init__(self, *args, filename='', **kwargs):
        self.db = QuotesDatabase(filename)
        super().__init__(*args, **kwargs)

    def _write_to_db(self, quotes, quote_key, author_key):
        self.db.add_list(quotes, quote_key, author_key)
        return True

    # @staticmethod
    # def __clean_data(data):
    #     new_data = []
    #     index = 0
    #     for quote in data:
    #         quote['id'] = index
    #         quote['used_on_insta'] = False
    #         quote['timestamp'] = str(datetime.now())
    #         new_data.append(quote)
    #         index += 1
    #     return new_data


if __name__ == '__main__':
    url = 'https://type.fit/api/quotes'
    test = QuotesTinyDb(url, method='get', filename="../Database/quotes_data.json", quote_key='text')
