"""
 -> Creates a db if there is not.
 -> Add more api to increase the size of our db
 -> Add more methods to increase the size of our db
"""
from Scripts.Database.tinyDb import QuotesDatabase
from dotenv import load_dotenv

"""
Go to file Scripts/AddQuotes/add_quotes_from_api.py for more
information regarding api fetching.
.
.
.
Big thanks to type.fit api developer for this amazing api for quotes    
"""

# Loading Env Variables
if not load_dotenv(verbose=True):
    raise ValueError('.env file not found.')

# The list of url to fetch quotes and add to our db
urls = [

    {
        'url': 'https://type.fit/api/quotes',
        'quote_key': 'text',
        'author_key': 'author',
        'method': 'get',
    }
]
# Assign it your preferred database
db = QuotesDatabase()
if db.is_empty():
    for url in urls:
        db.add_from_api(**url)
