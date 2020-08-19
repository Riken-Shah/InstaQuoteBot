from Instagram.Templates.Temaplete01 import Template as SimpleDesign

if __name__ == '__main__':
    template = SimpleDesign(for_test=False)
    for i in range(1, 101):
        did_create = template.generate_post()
        if did_create:
            did_create.save(f'Test/test{i}.png')
        template.update_everything()
