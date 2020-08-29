import os
import logging
from Scripts.Helpers.create_post import CreatePost
from Scripts.Helpers.greetings import greeting_to_new_users
from Scripts.Instagram.InstagramAPI import InstagramAPIBot
import schedule
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments you can use...')

    parser.add_argument('-t', '--testing', type=bool, help='Make it true if you are using it in Testing mode',
                        default=False)
    parser.add_argument('-lf', '--logfile', type=str, help='Logfile Path', default='app.log')
    parser.add_argument('-pp', '--post-img-path', type=str, help='Post image path',
                        default=f'{os.path.abspath(os.getcwd())}/post.png')

    args = parser.parse_args()
    # Setting Up a LogFile
    logging.basicConfig(level=logging.INFO, filename=args.logfile, filemode='w',
                        format='%(asctime)s - %(name)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info('CREATED LOGFILE')

    post = None
    try:
        post = CreatePost(testing=args.testing)
    except Exception as e:
        logging.exception('Error in CreatePost instance')

    instagram_api_bot = InstagramAPIBot(testing=args.testing)
    if post:
        path = args.post_img_path
        # Post a new quote
        schedule.every(6).hours.do(post.create, path)
        # Greet the new users
        schedule.every(3).hours.do(greeting_to_new_users, post.post_bot, instagram_api_bot)
        # Like Every Comment
        schedule.every(8).hours.do(instagram_api_bot.process_comment)

        while True:
            schedule.run_pending()
