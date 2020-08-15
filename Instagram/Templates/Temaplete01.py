from Instagram.InstaPost import InstaPost
from PIL.ImageColor import getcolor, getrgb
from PIL.ImageOps import grayscale
from PIL import Image, ImageDraw


class Template(InstaPost):
    def __init__(self, font_color: str = None, bg_color: str = None):
        """
        This class returns an instagram post with simplistic amazing design
        """
        super().__init__()
        if not font_color and not bg_color:
            self.theme_color = self.__generate_a_theme_color()
        else:
            self.theme_color = {'font_color': font_color, 'bg_color': bg_color}

    # Generates A Random Instagram Post
    def generate_post(self):
        img = self.__generate_template()
        font_color = self.theme_color['font_color']
        draw = ImageDraw.Draw(img)
        margin_bottom = 100

        # Write Quote and Author in Image
        text_box = (self.__get_percentage_of_size(0), (self._size[0] - margin_bottom - 50, self._size[1]))
        self.write_text(img, text_box, self.quote, font_color=font_color, top_bottom_padding=50, font_size=200,
                        font_path='/Library/Fonts/Ovo-Regular.ttf', max_top_bottom_padding=0)

        # Draw Line
        line_coords = ((0, self._size[1] - margin_bottom), (self._size[0], self._size[1] - margin_bottom))
        draw.line(line_coords, fill='#988978',
                  width=7)

        # Write Author
        author_text = ((0, self._size[1] - margin_bottom / 100 * 70), (self._size[0], self._size[1]))
        self.write_text(img, author_text,
                        text=self.author, font_size=50, font_color=font_color,
                        font_path='/Library/Fonts/Ovo-Regular.otf',
                        need_checking=False)
        return img

    # Return A Basic Template
    def __generate_template(self):
        return Image.new('RGB', self._size, color=self.theme_color['bg_color'])

    # Returns A Random Theme Color For The Post
    @staticmethod
    def __generate_a_theme_color():
        return {'font_color': '#312922', 'bg_color': '#FEE1C6'}

    # Takes an Img Object and return a tint image
    @staticmethod
    def __image_tint(src: str, tint='#ffffff'):
        if src:  # file path?
            src = Image.open(src)
        if src.mode not in ['RGB', 'RGBA']:
            raise TypeError('Unsupported source image mode: {}'.format(src.mode))
        src.load()

        tr, tg, tb = getrgb(tint)
        tl = getcolor(tint, "L")  # tint color's overall luminosity
        if not tl:
            tl = 1  # avoid division by zero
        tl = float(tl)  # compute luminosity preserving tint factors
        sr, sg, sb = map(lambda tv: tv / tl, (tr, tg, tb))  # per component
        # adjustments
        # create look-up tables to map luminosity to adjusted tint
        # (using floating-point math only to compute table)
        luts = (tuple(map(lambda lr: int(lr * sr + 0.5), range(256))) +
                tuple(map(lambda lg: int(lg * sg + 0.5), range(256))) +
                tuple(map(lambda lb: int(lb * sb + 0.5), range(256))))
        l = grayscale(src)  # 8-bit luminosity version of whole image
        if Image.getmodebands(src.mode) < 4:
            merge_args = (src.mode, (l, l, l))  # for RGB version of grayscale
        else:  # include copy of src image's alpha layer
            a = Image.new("L", src.size)
            a.putdata(src.getdata(3))
            merge_args = (src.mode, (l, l, l, a))  # for RGBA version of grayscale
            luts += tuple(range(256))  # for 1:1 mapping of copied alpha values

        return Image.merge(*merge_args).point(luts)

    # Return A Percentage of Instagram Post
    def __get_percentage_of_size(self, per):
        return self._size[0] / 100 * per, self._size[1] / 100 * per
