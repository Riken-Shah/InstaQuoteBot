"""
Here will be all the constructor or methods to add quotes to our db
"""
from AddQuotes.add_quotes_from_api import AddFromApi

if __name__ == '__main__':
    # TypeFit
    type_fit_url = 'https://type.fit/api/quotes'
    typeFit = AddFromApi(url=type_fit_url, quote_key='text')
