from mediawiki import MediaWiki
from mediawiki.exceptions import PageError
import random
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError


class BasicCaption:
    def __init__(self, page_name='bot.quote'):
        self.author = None
        self.page_name = page_name
        self.wikipedia = MediaWiki(timeout=20)
        self.__max_chars = 2200
        self.__hashtag_limit = 30
        self.__username_limit = 30

    def create_caption(self, author):
        """
        Creates a caption
        """
        self.author = author
        caption = f' 👉 A Beautiful Quote By #{self.author.title().replace(" ", "")} 👈. '
        caption += f'Follow my 👉 @{self.page_name} 👈 for more inspirational quote 🙇‍ like this.️'.strip()
        if author != 'Anonymous':
            try:
                page = self.__get_request()
            except ReadTimeout:
                try:
                    page = self.__get_request()
                except ReadTimeout:
                    caption += self.__add_space(3)
                    return caption + self.__hashtags()
            if not page:
                caption += self.__add_space(3)
                return caption + self.__hashtags()
            # Adding Call to action
            caption += self.__call_to_action()
            # Adding Space
            caption += self.__add_space(2)
            # Adding author summary
            caption += page.summarize(chars=400)
            # Adding space
            caption += self.__add_space(4)
            # Adding Wikipedia link
            caption += f' Read more on {page.url}'
            # Adding space
            caption += self.__add_space(3)
            caption += self.__hashtags()
        return caption

    @staticmethod
    def __add_space(lines: int, char='.'):
        """
        Returns a string with space
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