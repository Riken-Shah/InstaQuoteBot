import unittest
import os

# Changing working directory to root
if not os.path.exists('Scripts') and os.path.exists('test_instagram.py'):
    os.chdir('..')

from Scripts.Helpers.instagram import post_on_instagram
from Scripts.Instagram.InstagramAPI import InstagramAPIBot
from Scripts.Instagram.Templates.Temaplete01 import Template as SimpleDesign
from Scripts.Instagram.CaptionCreator import BasicCaption
from Scripts.Instagram.SeleniumBot import SeleniumBot


class TestInstagram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Creating a template instance
        cls.template = SimpleDesign()
        # Creating a caption instance
        cls.caption_template = BasicCaption()
        # Creating a bot instance
        cls.selenium_bot = SeleniumBot(testing=True)
        # Creating instagram API instance
        cls.instagram_api_bot = InstagramAPIBot(testing=True)

    @classmethod
    def tearDownClass(cls):
        cls.selenium_bot.exit()

    def test_generate_image(self):
        response = self.template.generate_post()
        self.assertTrue(response)

    def test_post_on_instagram(self):
        response = post_on_instagram(self.selenium_bot, self.template, self.caption_template)
        self.assertTrue(response)

    def test_greet_new_user(self):
        response = self.selenium_bot.greet_new_users(['instagram'])
        self.assertTrue(response)

    def test_comment_like(self):
        post = self.instagram_api_bot.get_last_post()
        if not post:
            self.test_post_on_instagram()
            post = self.instagram_api_bot.get_last_post()

        self.selenium_bot.comment(post['code'], 'Test Comment')
        response = self.instagram_api_bot.process_comment()
        self.assertTrue(response)


if __name__ == '__main__':
    unittest.main()
