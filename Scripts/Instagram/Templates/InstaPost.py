from PIL import ImageDraw, ImageFont
from Scripts.Database.tinyDb import QuotesDatabase


class InstaPost(QuotesDatabase):
    """
    *This class expects an database object
    (You can pass your custom db to it)

    You can use this class as a base class when you are writing a new template for your instagram post
    It has feature like like writing responsive text, generating
    quotes and author.
    """
    def __init__(self, *args, **kwargs):
        # Default Instagram Post Size
        self._size = (1080, 1080)
        self.default_font = 'Fonts/Ovo-Regular.ttf'
        self.__font_size_smallest = 30
        self.__padding_top_bottom_smallest = 20

        super().__init__(*args, **kwargs)
        self.quote = None
        self.author = None
        self.fetch_new()
        if not self.quote or not self.author:
            raise ValueError('Quote or Author Not Found')

    def fetch_new(self):
        """
        Set Quote and Author
        """
        res = self.fetch_quote()
        if res:
            self.quote = res['quote']
            self.author = res['author'] or 'Anonymous'

    @staticmethod
    def _clean_quote(text, max_char_in_sentence=50):
        """
        The functions returns the text in phrase to avoid text overflowing
        :param max_char_in_sentence: Max number of chars in a sentence
        :return: list of sentence
        """
        clean_text = ['']
        word = ''
        count = 0
        for i in range(len(text)):
            word += text[i]
            if text[i] == ' ' or text[i] == '.' or text[i] == ',' or text[i] == '-' or len(text) - 1 == i and word:
                if len(clean_text[count]) + len(word) > max_char_in_sentence:
                    count += 1
                    clean_text.append('')
                clean_text[count] += word.lstrip()
                word = ''
        # Cleaning (removing empty strings)
        for text_block in clean_text:
            if not text_block:
                del clean_text[clean_text.index(text_block)]
        return clean_text

    def __set_text_in_image(self, img, x: int, y: int, texts: list, side_padding=50, top_bottom_padding=80,
                            font_path=None, font_size=50, font_color=(0, 0, 0), max_top_bottom_padding=None):
        """
        This function set text in image
        :param img: Expects a PIL image instance
        :param x: X-axis you want to start writing from
        :param y: Y-axis you want to start writing from
        :param texts: List of strings (Make sure each str does not exceeds max_chars in line)
        :param side_padding: Left Right Padding
        :param top_bottom_padding: Space between each line
        :param font_path: Path to the font
        :param font_size: Font size
        :param font_color: Font color
        :param max_top_bottom_padding: Max top bottom padding
        :return: None
        """
        if not font_path:
            font_path = self.default_font
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

    def write_text(self, img, xy, text, font_size=70, top_bottom_padding=30, side_padding=50, need_checking=True,
                   **kwargs):
        """
        This function set the test in image, it will calculate max number of lines needed, max number character allowed
        each line.
        :param img: Expects a PIL image instance
        :param xy: Expects image dimensions
        :param text: Expects image dimensions
        :param font_size: Expects image dimensions
        :param top_bottom_padding: Space between each line
        :param side_padding: Left Right Padding
        :param need_checking: If it is False then value like max_lines, max_chars will not
        automatically set
        :return: None
        """
        # Get the height and width of the text box
        height, width = self.__get_width_and_height(xy)
        max_chars = None
        while True and need_checking:
            # Get the max number of lines
            max_lines = self.__get_max_lines(text, height, font_size, top_bottom_padding)

            # Get the max chars in a line
            max_chars = self.__get_max_chars(text, font_size, max_width=width - side_padding / 100 * 0)

            # Wrap the text
            text_wrapper = self._clean_quote(text, max_chars)

            if max_lines >= len(text_wrapper):
                break

            if font_size >= self.__font_size_smallest:
                font_size -= 5
            else:
                return False

            if top_bottom_padding >= self.__padding_top_bottom_smallest:
                top_bottom_padding -= 2

        if not need_checking:
            max_chars = 50

        # Writing to the image
        self.__set_text_in_image(img, xy[0][0], xy[0][1], self._clean_quote(text, max_chars),
                                 font_size=font_size,
                                 top_bottom_padding=top_bottom_padding, side_padding=side_padding + 30, **kwargs)
        return True

    def __get_max_lines(self, text, height, font_size, top_bottom_padding):
        """
        Calculates and return max number of lines a quote will need
        """
        font = ImageFont.truetype(self.default_font, size=font_size)
        _, f_height = font.getsize(text)
        return int(height / (f_height + top_bottom_padding))

    def __get_max_chars(self, text, font_size, max_width, max_chars=50):
        """
        Calculates and return max number of character in lines a quote will need
        """
        max_width -= 50
        while True:
            text = text[:max_chars]
            font = ImageFont.truetype(self.default_font, size=font_size)
            f_width, _ = font.getsize(text)
            if f_width <= max_width:
                break
            max_chars -= 1
        return 1 if max_chars - 1 < 0 else max_chars - 1

    @staticmethod
    def __get_width_and_height(xy):
        """
        This function return length and width from xy coordinates
        :param xy:
        :return: length: float, width: float
        """
        return xy[1][0] - xy[0][0], xy[1][1] - xy[0][1]
