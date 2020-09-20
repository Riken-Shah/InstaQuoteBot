import Tests
from Scripts.Helpers.create_post import CreatePost
from Scripts.Instagram.InstagramAPI import InstagramAPIBot
import os

if __name__ == '__main__':
    test_post_path = os.path.abspath(os.getcwd() + 'test.png')
    post = CreatePost(testing=True)
    api_bot = InstagramAPIBot(testing=True)

    # Post Test
    post.create(test_post_path)
    # Greet Message
    post.post_bot.first_time_following(['instagram', 'riken.py'])
    # Comment Like
    api_bot.process_comment()
    # Removing Test Image
    os.remove(test_post_path)
    # Closing Bot
    post.post_bot.exit()
    print('Test Successfully Passed')
