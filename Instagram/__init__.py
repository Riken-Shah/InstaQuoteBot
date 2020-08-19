from Instagram.Templates.Temaplete01 import Template as SimpleDesign

if __name__ == '__main__':
    template = SimpleDesign(for_test=False)
    for i in range(1, 100):
        post = template.generate_post()
        post.save(f'Test/test{i}.png')
        template.update_everything()
        print(f'{(101 - i - 1)/100 * 100}% left', i)