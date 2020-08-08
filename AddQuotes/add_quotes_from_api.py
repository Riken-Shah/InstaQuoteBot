import requests
import json
from database import QuotesDatabase


class AddFromApi:
    def __init__(self, url, quote_key='quote', author_key='author', method='get' or 'post', headers=None):
        """
        :param url: Url of an api
        :param quote_key: The text to access `quote` in response
        :param author_key: The text to access `author` in response
        :param method: Either 'get' or 'post'
        :param headers: Headers to pass through request
        :return: True
        """
        # Init the Database and requests
        self.requests = requests
        # Give your path to Firebase Admin SDK Cred
        self.db = QuotesDatabase('../intagram-bot-firebase-adminsdk-slaoe-3e8bc1ca0a.json')

        # Send Request
        response = self.__send_request(url, method.lower(), headers)
        if response.status_code == 200:
            self.__write_to_db(json.loads(response.content), quote_key, author_key)
        else:
            ConnectionError('API is not configured properly')

    # Sends the request
    def __send_request(self, url, method, headers):
        if not (method == 'get' or method == 'post'):
            raise ValueError('method should only be `get` or `post` ')

        request = getattr(self.requests, method)
        return request(url=url, headers=headers)

    # Write quotes to the database
    def __write_to_db(self, quotes, quote_key, author_key):
        self.db.add_list(quotes, quote_key, author_key)
        return True
