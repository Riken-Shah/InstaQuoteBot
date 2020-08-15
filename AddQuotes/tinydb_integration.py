from AddQuotes.add_quotes_from_api import AddFromApi
import requests
import json
from datetime import datetime


class TinyDB:
    def __init__(self, url, methods, headers, filename):
        self.response = AddFromApi.send_request(requests, url=url, method=methods, headers=headers)
        self.filename = filename
        if self.response.status_code != 200:
            ConnectionError('API did not give the correct response')
        self.__write_json_file()

    def __write_json_file(self):
        data = self.response.content
        if not data:
            return ValueError('Response has no data.')

        clean_data = self.__clean_data(json.loads(data))
        with open(self.filename, 'w+') as file:
            for line in json.dumps(clean_data, sort_keys=True, indent=4, default=str):
                file.write(line)

    @staticmethod
    def __clean_data(data):
        new_data = []
        index = 0
        for quote in data:
            quote['id'] = index
            quote['used_on_insta'] = False
            quote['timestamp'] = datetime.now()
            new_data.append(quote)
            index += 1
        return new_data


if __name__ == '__main__':
    url = 'https://type.fit/api/quotes'
    test = ApiToJson(url, 'get', None, filename="quotes_data.json")
