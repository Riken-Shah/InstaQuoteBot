import os
from Scripts.Instagram.Templates.Temaplete01 import Template as SimpleDesign
from Scripts.Instagram.CaptionCreator import BasicCaption
from Scripts.Instagram.Bot import Bot


class CreatePost:
    def __init__(self, testing=False):
        # Creating a template instance
        self.template = SimpleDesign(for_test=testing)

        # Creating a caption instance
        self.caption_template = BasicCaption()

        # Creating a bot instance
        self.post_bot = Bot(testing=testing)

    def create(self, img_path, counter=0):
        did_create = self.template.generate_post()
        if did_create:
            did_create.save(img_path)
            print(self.template.quote, self.template.author)
            caption = self.caption_template.create_caption(self.template.author)
            self.post_bot.post(img_path, caption)
            self.template.update_everything()
            return True
        # Re-run for 10 times if it failed
        elif counter < 10:
            print(f'Failed for creating a post... Running again for {counter} time.')
            counter += 1
            return self.create(img_path, counter=counter)
        return False


