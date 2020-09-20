import os
from instagram_private_api import Client
from tinydb import TinyDB, where


class InstagramAPIBot:
    def __init__(self, max_comments_to_reply=50, testing=False):
        self.__username = os.getenv('username')
        self.__password = os.getenv('password')

        if not self.__username or not self.__password:
            raise ValueError('Username or Password Not Found in Local Environment')

        self.__api = Client(self.__username, self.__password)
        self.__max_comments_to_reply = max_comments_to_reply
        self.__user_db = TinyDB('user_database.json')
        self.testing = testing

        if testing:
            self.api = self.__api

    def __get_self_feed(self):
        """
        Returns a list of your own post
        """
        feed = []
        response = self.__api.self_feed()
        feed += response['items']
        while response['more_available']:
            response = self.__api.self_feed(max_id=response['next_max_id'])
            feed += response['items']
        return feed

    def __get_comments(self, media_id: str):
        """
        Returns the comments from the post
        max: self.__max_comments_to_reply
        """
        comments = []
        response = self.__api.media_comments(media_id)
        comments += response['comments']
        while response['has_more_comments']:
            response = self.__api.media_comments(media_id, max_id=response['next_max_id'])
            comments += response['comments']

            if len(comments) > self.__max_comments_to_reply:
                break

        return comments[:self.__max_comments_to_reply]

    def __get_all_followers(self):
        """
        Returns a all followers
        """
        users = []
        response = self.__api.user_followers(user_id=self.__api.authenticated_user_id,
                                             rank_token=self.__api.generate_uuid())
        users += response['users']
        while response['next_max_id']:
            response = self.__api.user_followers(user_id=self.__api.authenticated_user_id,
                                                 rank_token=self.__api.generate_uuid(),
                                                 max_id=response['next_max_id'],
                                                 )
            users += response['users']

        return users

    def process_comment(self):
        """
        Likes Every Comment from all posts
        """
        if self.testing:
            posts = [self.__api.username_feed('instagram')['items'][0]]
        else:
            posts = self.__get_self_feed()
        for post in posts:
            comments = self.__get_comments(post['pk'])
            for comment in comments:
                if not comment['has_liked_comment']:
                    self.__api.comment_like(comment['pk'])

    def get_new_user_followers(self):
        """
        Returns a list of new users
        """
        users = self.__get_all_followers()
        new_users = []
        for user in users:
            if not self.__user_db.search(where('pk') == user['pk']):
                self.__user_db.insert(user)
                new_users.append(user)
        return new_users



