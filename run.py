import os
import logging
from Scripts.create_post import CreatePost
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
    if post:
        path = args.post_img_path
        schedule.every(6).hours.do(post.create, path)
        post.create(path)

        while True:
            schedule.run_pending()
