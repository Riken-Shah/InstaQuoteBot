from mediawiki import MediaWiki
from mediawiki.exceptions import PageError
import random
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError
from PyDictionary import PyDictionary
from random import shuffle
import os


class BasicCaption:
    def __init__(self):
        self.author = None
        self.page_name = os.getenv('username')
        self.wikipedia = MediaWiki(timeout=20)
        self.__max_chars = 2200
        self.__hashtag_limit = 30
        self.__username_limit = 30
        self.dictionary = PyDictionary()

    def create_caption(self, author):
        """
        Creates a caption
        """
        self.author = author
        caption = f' 👉 A {self.__get_random_adjective()} Quote By #{self.author.title().replace(" ", "")} 👈. '
        caption += f'Follow my page 👉 @{self.page_name} 👈 for more inspirational quote 🙇‍ like this.️'.strip()
        page = None
        if author != 'Anonymous':
            try:
                page = self.__get_request()
            except ReadTimeout:
                # Try again
                try:
                    page = self.__get_request()
                except ReadTimeout:
                    pass
            if not page:
                caption += self.__add_new_line(3)
                return caption + self.__hashtags()
            # Adding Call to action
            caption += self.__call_to_action()
            # Adding Space
            caption += self.__add_new_line(2)
            # Adding author summary
            caption += page.summarize(chars=400)
            # Adding space
            caption += self.__add_new_line(4)
            # Adding Wikipedia link
            caption += f' Read more on {page.url}'
            # Adding space
            caption += self.__add_new_line(3)
            caption += self.__hashtags()
        return caption

    def __get_random_adjective(self):
        """
        Returns a random adjective
        """
        basic_words = ['beautiful', 'amazing', 'wonderful']
        shuffle(basic_words)
        random_base_word = basic_words[0]
        synonyms = self.dictionary.synonym(random_base_word)
        shuffle(synonyms)
        return synonyms[0]

    @staticmethod
    def __add_new_line(lines, char='.'):
        """
        Returns a string with new line
        """
        space = '\n'
        for _ in range(lines):
            space += f'{char} \n'
        return space

    @staticmethod
    def __hashtags():
        """
        Returns a str of hashtags
        """
        return '#quote #quoteoftheday #quotes #quotestagram #quotesindonesia #quotestoliveby #quotesaboutlife ' \
               '#quotesdaily #lovequotes #motivationalquotes #quotesoftheday #quoted #quotesgalau ' \
               '#inspirationalquotes #quotestags #quotesandsayings #quotescinta #quoteskeren #quotestoinspire '

    @staticmethod
    def __call_to_action():
        """
        Randomly returns a call to action text
        """
        call_to_action = [
            'Rate this quote below 👇',
            'Did you like this quote ❓',
            'Read more about the author below 👇',
            'What do you think about this quote ⸮',
            ]
        return call_to_action[random.randrange(0, len(call_to_action) - 1)]

    def __get_request(self):
        """
        Returns a wikipedia page response if exists
        """
        response = None
        try:
            response = self.wikipedia.page(self.__clean_author())
        except (PageError, ConnectionError):
            pass

        return response

    def __clean_author(self):
        """
        Returns a readable author name for WikiMedia
        """
        return self.author.replace(' ', '_')
