from Instagram.Templates.Temaplete01 import Template as SimpleDesign

if __name__ == '__main__':
    post = SimpleDesign().generate_post()
    post.save('test.png')
