from Scripts.Helpers.create_post import CreatePost
from Scripts.Instagram.InstagramAPI import InstagramAPIBot
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Commands')

    parser.add_argument('-ch', '--chromeHead', type=bool, help='You chrome instance should not be headless',
                        default=False)

    args = parser.parse_args()

    test_post_path = os.path.abspath(os.getcwd() + 'test.png')
    post = CreatePost(testing=args.chromeHead)
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
