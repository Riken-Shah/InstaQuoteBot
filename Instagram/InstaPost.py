from PIL import  ImageDraw, ImageFont
from database import QuotesDatabase


class InstaPost(QuotesDatabase):
    """
    This class has a base class which has base function to
    create instagram post like writing responsive text, generating
    quotes and author.
    """
    # Default Instagram Post Size
    _size = (1080, 1080)
    default_font = '/Library/Fonts/AppleMyungjo.ttf'
    __font_size_smallest = 30
    __padding_top_bottom_smallest = 20

    def __init__(self):
        super().__init__('/Volumes/Samsung USB/PycharmProjects/IntagramBot/intagram-bot-firebase-adminsdk-slaoe'
                         '-3e8bc1ca0a.json')
        res = self.fetch_quote(for_test=True)
        self.quote = res['quote']
        self.author = res['author']

    # Clean the Text
    @staticmethod
    def _clean_quote(text, max_char_in_sentence: int = 50):
        """
        The functions returns the text in phrase to avoid text overflowing
        :param max_char_in_sentence: Max number of chars in a sentence
        :return: list of sentence
        """
        clean_text = []
        count = 0
        sentence = ''
        is_word = False

        for i in range(len(text)):
            if count >= max_char_in_sentence and is_word:
                clean_text.append(sentence)
                count = 0
                sentence = ''
            count += 1
            sentence += text[i]
            is_word = text[i] == ' ' or text[i] == '.'
        clean_text.append(sentence)

        return clean_text

    # Set the text in Image
    @staticmethod
    def __set_text_in_image(img, x: int, y: int, texts: list, side_padding=50, top_bottom_padding=80,
                            font_path=default_font, font_size=50, font_color=(0, 0, 0), max_top_bottom_padding=None):

        fnt = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(img)
        margin = None

        for text in texts:
            draw.text((x + side_padding / 2, y), text, font=fnt, fill=font_color)
            _, h = fnt.getsize(text)
            if not margin:
                margin = h + top_bottom_padding
                if max_top_bottom_padding and margin > max_top_bottom_padding:
                    margin = max_top_bottom_padding

            y += margin

    def write_text(self, img, xy, text, font_size=70, top_bottom_padding=30, side_padding=50, need_checking=True, **kwargs):
        # Get the height and width of the text box
        height, width = self.__get_width_and_height(xy)
        max_chars = None
        while True and need_checking:
            # Get the max number of lines
            max_lines = self.__get_max_lines(text, height, font_size, top_bottom_padding)

            # Get the max chars in a line
            max_chars = self.__get_max_chars(text, font_size, max_width=width - side_padding / 100 * 50)

            # Wrap the text
            text_wrapper = self._clean_quote(text, max_chars)

            if max_lines >= len(text_wrapper):
                break

            if font_size >= self.__font_size_smallest:
                font_size -= 5
            else:
                # break
                return False

            if top_bottom_padding >= self.__padding_top_bottom_smallest:
                top_bottom_padding -= 5

        if not need_checking:
            max_chars = 50

        # Writing to the image
        self.__set_text_in_image(img, xy[0][0], xy[0][1], self._clean_quote(text, max_chars),
                                 font_size=font_size,
                                 top_bottom_padding=top_bottom_padding, side_padding=side_padding + 30, **kwargs)
        return True

    def __get_max_lines(self, text, height, font_size, top_bottom_padding):
        font = ImageFont.truetype(self.default_font, size=font_size)
        _, f_height = font.getsize(text)

        return int(height / (f_height + top_bottom_padding))

    def __get_max_chars(self, text, font_size, max_width, max_chars=50):
        while True:
            text = text[:max_chars]
            font = ImageFont.truetype(self.default_font, size=font_size)
            f_width, _ = font.getsize(text)
            if f_width <= max_width:
                break
            max_chars -= 1
        return 1 if max_chars - 5 < 0 else max_chars - 5

    @staticmethod
    def __get_width_and_height(xy):
        """
        This function return length and width from xy coordinates
        :param xy:
        :return: length: float, width: float
        """
        return xy[1][0] - xy[0][0], xy[1][1] - xy[0][1]
