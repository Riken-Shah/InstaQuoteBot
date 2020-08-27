"""
 -> Creates a db if there is not.
 -> Add more api to increase the size of our db
 -> Add more methods to increase the size of our db
"""
import os
from Scripts.AddQuotes.tinydb_integration import QuotesTinyDb
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
    }
]

# Setting up db file path
file_path = os.getenv('tiny_db_path_to_db')
if file_path:
    if not os.path.exists(file_path):
        # Setting up the Database
        open(file_path, 'w')
        for url in urls:
            QuotesTinyDb(**url)
else:
    raise ValueError(' `tiny_db_path_to_db` variable not found in .env file')
