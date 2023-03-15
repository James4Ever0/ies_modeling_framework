from jinja2 import Environment,FileSystemLoader

#template = open('jinja_test.j2','r').read()

#mylist = [1,2,3]
def main():
    env = Environment(loader = FileSystemLoader('./'))
    tpl = env.get_template('jinja_test.j2')
    
    with open('page.txt','w+') as fout:
        render_content = tpl.render(mylist = [1,2,3])
        fout.write(render_content)
        
if __name__ == '__main__':
    main()
# print:
# prefix 1
# prefix 2
# prefix 3