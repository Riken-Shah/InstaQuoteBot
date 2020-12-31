import os
import argparse

from Scripts.Helpers.instagram import post_on_instagram
from Scripts.Instagram.InstagramAPI import InstagramAPIBot
from Scripts.Instagram.Templates.Temaplete01 import Template as SimpleDesign
from Scripts.Instagram.CaptionCreator import BasicCaption
from Scripts.Instagram.SeleniumBot import SeleniumBot


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Commands')

    parser.add_argument('-hl', '--headless', type=bool, help='You chrome instance should not be headless',
                        default=False)

    args = parser.parse_args()

    # Creating a template instance
    template = SimpleDesign()
    # Creating a caption instance
    caption_template = BasicCaption()
    # Creating a bot instance
    selenium_bot = SeleniumBot(testing=not args.headless)
    # Creating instagram API instance
    instagram_api_bot = InstagramAPIBot(testing=not args.headless)
    # Post Test
    test_img_path = os.path.abspath(os.getcwd() + 'test.png')
    post_on_instagram(selenium_bot, template, caption_template, img_path=test_img_path)
    # Greet Message
    selenium_bot.greet_new_users(['instagram'])
    # Comment Like
    instagram_api_bot.process_comment()
    # Removing Test Image
    os.remove(test_img_path)
    # Shutting Down Bot
    selenium_bot.exit()
    print('Test Successfully Passed')
