import os


def post_on_instagram(selenium_bot, template, caption_template, img_path=None):
    """
    Post on instagram
    :param selenium_bot: expects Scripts.Instagram.Bot Instance
    :param template: expects Scripts.Instagram.Templates.* Instance
    :param caption_template: expects Scripts.Instagram.CaptionCreator Instance
    :param img_path: str where you want to save image
    :return: Boolean Value if it is created or not
    """
    if not img_path:
        img_path = os.path.abspath(os.getcwd() + 'test.png')

    did_create = template.generate_post()
    if did_create:
        did_create.save(img_path)
        caption = caption_template.create_caption(template.author)
        selenium_bot.post(img_path, caption)
        template.update_everything()
    return did_create


def greeting_to_new_users(selenium_bot, api_bot):
    """"
    Greeting for New User
    :param selenium_bot: expects Scripts.Instagram.CaptionCreator Instance
    :param api_bot: expects Scripts.Instagram.InstagramAPI Instance
    :return: None

    """
    new_users = api_bot.get_new_user_followers()
    new_users = list(map(lambda user: user['username'], new_users))
    if new_users:
        selenium_bot.greet_new_users(new_users)

