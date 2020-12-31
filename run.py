import os
import logging
from Scripts.Helpers.instagram import greeting_to_new_users, post_on_instagram
from Scripts.Instagram.InstagramAPI import InstagramAPIBot
from Scripts.Instagram.Templates.Temaplete01 import Template as SimpleDesign
from Scripts.Instagram.CaptionCreator import BasicCaption
from Scripts.Instagram.SeleniumBot import SeleniumBot

import schedule
import argparse


def main():
    # Creating a template instance
    template = SimpleDesign()
    # Creating a caption instance
    caption_template = BasicCaption()
    # Creating a bot instance
    selenium_bot = SeleniumBot(testing=args.testing)
    # Creating instagram API instance
    instagram_api_bot = InstagramAPIBot(testing=args.testing)

    # Post a new quote
    schedule.every(6).seconds.do(post_on_instagram, selenium_bot, template, caption_template,
                                 img_path=args.post_img_path)
    # Greet the new users
    schedule.every(3).seconds.do(greeting_to_new_users, selenium_bot, instagram_api_bot)
    # Like Every Comment
    schedule.every(8).seconds.do(instagram_api_bot.process_comment)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments you can use...')

    parser.add_argument('-t', '--testing', type=bool, help='True if you are using it in Testing mode',
                        default=False)
    parser.add_argument('-lf', '--logfile', type=str, help='Logfile Path', default='app.log')
    parser.add_argument('-pp', '--post-img-path', type=str, help='Post image path',
                        default=f'{os.path.abspath(os.getcwd())}/post.png')
    parser.add_argument('-r', '--max-retry', type=int, help='Max retry count', default=10)

    args = parser.parse_args()
    # Setting Up a LogFile
    logging.basicConfig(level=logging.INFO, filename=args.logfile, filemode='w',
                        format='%(asctime)s - %(name)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info('CREATED LOGFILE')
    while args.max_retry >= 0:
        try:
            main()
        except Exception:
            logging.exception('Something went wrong.')
        args.max_retry -= 1
