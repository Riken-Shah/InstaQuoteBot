from Instagram.Templates.Temaplete01 import Template as SimpleDesign
from Instagram.CaptionCreator import BasicCaption
from Instagram.Bot import Bot
import os
from dotenv import load_dotenv


if __name__ == '__main__':
    # Loading Local Environment Variables
    template = None
    if not load_dotenv():
        raise EnvironmentError(".env file is not setup properly")
    try:
        template = SimpleDesign(for_test=False)
    except ValueError as e:
        print(e)
    caption_template = BasicCaption()
    post_bot = Bot(testing=True)
    for i in range(1, 100):
        did_create = template.generate_post()
        if did_create:
            path = f'Test/test{i}.png'
            did_create.save(path)
            caption = caption_template.create_caption(template.author)
            post_bot.post(f'{os.path.abspath(os.getcwd())}/{path}', caption)

        template.update_everything()
