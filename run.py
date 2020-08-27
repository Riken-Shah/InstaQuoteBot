import os
import logging
from create_post import CreatePost
import schedule

if __name__ == '__main__':
    # Setting Up a LogFile
    logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                        format='%(asctime)s - %(name)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info('CREATED LOGFILE')

    post = None
    counter = 0
    try:
        post = CreatePost()
    except Exception as e:
        logging.exception('Error in CreatePost instance')
    if post:
        path = os.path.abspath(os.getcwd()) + '/post.png'
        schedule.every(6).hours.do(post.create, path)
        post.create(path)

        while True:
            schedule.run_pending()
