from Scripts.Instagram.Templates.Temaplete01 import Template as SimpleDesign
from Scripts.Instagram.CaptionCreator import BasicCaption
from Scripts.Instagram.Bot import Bot
import logging


class CreatePost:
    def __init__(self, testing=False):
        # Creating a template instance
        self.template = SimpleDesign(for_test=testing)

        # Creating a caption instance
        self.caption_template = BasicCaption()

        # Creating a bot instance
        self.post_bot = Bot(testing=testing)
        logging.info('Created a Selenium Instance')

    def create(self, img_path, counter=0):
        did_create = self.template.generate_post()
        if did_create:
            did_create.save(img_path)
            caption = self.caption_template.create_caption(self.template.author)
            try:
                self.post_bot.post(img_path, caption)
            except Exception:
                logging.exception('Something Went Wrong with the Bot')
                logging.info('Restarting the bot...')
                self.post_bot = Bot(testing=False)
                self.create(img_path, counter=counter)
            self.template.update_everything()
            return True
        # Re-run for 10 times if it failed
        elif counter < 10:
            logging.error(f'Failed for creating a post... Running again for {counter} time.')
            counter += 1
            return self.create(img_path, counter=counter)
        return False


