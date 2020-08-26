import os
from create_post import CreatePost

if __name__ == '__main__':
    post = CreatePost()
    for i in range(1):
        path = os.path.abspath(os.getcwd()) + '/' + f'test{i + 1}.png'
        post.create(path)
    post.post_bot.exit()

""" 
TODO: 
1) Create a better file structure 
3) Finding a way to make every task occur at specific time 
4) Adding requirements.txt 
"""
