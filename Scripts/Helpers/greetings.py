from Scripts.Instagram.Bot import Bot
from Scripts.Instagram.InstagramAPI import InstagramAPIBot


def greeting_to_new_users(bot: Bot, api_bot: InstagramAPIBot):
    new_users = api_bot.get_new_user_followers()
    new_users = list(map(lambda user: user['username'], new_users))
    bot.first_time_following(new_users)
