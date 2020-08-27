import requests
import json


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

        # Send Request
        response = self.send_request(self.requests, url, method.lower(), headers)
        if response.status_code == 200:
            self._write_to_db(json.loads(response.content), quote_key, author_key)
        else:
            ConnectionError('API is not configured properly')

    # Sends the request
    @staticmethod
    def send_request(req, url, method, headers):
        """
        This function returns a api response
        :param req: requests instance
        :param url: api url
        :param method: api method
        :param headers: api headers
        :return: requests instance
        """
        if not (method == 'get' or method == 'post'):
            raise ValueError('method should only be `get` or `post` ')

        request = getattr(req, method)
        return request(url=url, headers=headers)

    # Write quotes to the database
    def _write_to_db(self, quotes, quote_key, author_key):
        """
        Overwrite this function to write a data to the database
        """
        return True
