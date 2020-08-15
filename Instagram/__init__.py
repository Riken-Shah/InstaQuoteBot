from Instagram.Template01.Temaplete01 import Template as SimpleDesign

if __name__ == '__main__':
    post = SimpleDesign().generate_post()
    post.save('test.png')
