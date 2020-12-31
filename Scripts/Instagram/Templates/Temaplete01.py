from Scripts.Instagram.Templates.InstaPost import InstaPost
from PIL.ImageColor import getrgb
from PIL import Image, ImageDraw
import randomcolor
import wcag_contrast_ratio as contrast


class Template(InstaPost):
    def __init__(self, font_color: str = None, bg_color: str = None, *args, **kwargs):
        """
        Demo Template 1
        This class returns an instagram post with simplistic amazing design
        """
        super().__init__(*args, **kwargs)
        if not font_color and not bg_color:
            self.theme_color = self._generate_a_theme_color()
        else:
            self.theme_color = {'font_color': font_color, 'bg_color': bg_color}

    def generate_post(self):
        """
        This function will create instagram post.
        """
        img = self.__generate_template()
        font_color = self.theme_color['font_color']
        draw = ImageDraw.Draw(img)
        margin_bottom = 100

        # Write Quote and Author in Image
        text_box = (self.__get_percentage_from_size(0), (self._size[0] - margin_bottom - 50, self._size[1]))
        did_write = self.write_text(img, text_box, self.quote, font_color=font_color, top_bottom_padding=50,
                                    font_size=200, max_top_bottom_padding=0)
        if not did_write:
            return False

        # Draw Line
        line_coords = ((0, self._size[1] - margin_bottom), (self._size[0], self._size[1] - margin_bottom))
        draw.line(line_coords, fill=self.theme_color['line_color'],
                  width=7)

        # Write Author
        author_text = ((0, self._size[1] - margin_bottom / 100 * 70), (self._size[0], self._size[1]))
        did_write = self.write_text(img, author_text,
                                    text=self.author, font_size=50, font_color=font_color,
                                    need_checking=False)
        if not did_write:
            return False

        return img

    # Update
    def update_everything(self):
        """
        This function is used to avoid re-init of class by
        setting new quote, author and theme
        """
        self.fetch_new()
        self.theme_color = self._generate_a_theme_color()

    def __generate_template(self):
        """
        Returns a base image
        """
        return Image.new('RGB', self._size, color=self.theme_color['bg_color'])

    def _generate_a_theme_color(self):
        """
        This function will return a random theme color that passes AAA contrast test
        """
        random_colors = randomcolor.RandomColor().generate(count=20)
        last_color = None
        for color in random_colors:
            if random_colors.index(color) % 2 == 0 and last_color:
                # Normalizing color
                first_color = tuple(map(lambda x: x / 255, getrgb(last_color)))
                second_color = tuple(map(lambda x: x / 255, getrgb(color)))
                is_passed = contrast.passes_AAA(contrast.rgb(first_color, second_color))
                if is_passed:
                    # Give lighter color to background
                    if color[0] + color[1] + color[2] > last_color[0] + last_color[1] + last_color[2]:
                        return {'font_color': last_color, 'bg_color': color, 'line_color': last_color}
                    else:
                        return {'font_color': color, 'bg_color': last_color, 'line_color': color}
            else:
                last_color = color
        return self._generate_a_theme_color()

    def __get_percentage_from_size(self, per):
        """
        Returns xy coordinates of % image size
        """
        return self._size[0] / 100 * per, self._size[1] / 100 * per
