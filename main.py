import web

urls = (
    '/','index',
    '/renderTest','Test',
    '/Todolists','todo.TD',
    '/TOdolists/(\w+)','todo.TD_Simple',
)

render = web.templates.render('templates')
config = web.storage(email='milofromlou@gmail.com',
                     site_name='Task Tracing',
                     site_desc='',
                     static='static'
                    )

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render

class Test:
    def GET(self):
        return render.showRender('hello world')

class index:
    def GET(self):
        return "Hello,world!"

    def POST(self):
        i = web.input()
        print(i)

from pymongo import MongoClient

client = MongoClient('localhost',27017)

db = client.todo_db

collection = db['Todolists']

if __name__ == '__main__':
    app = web.application(urls,globals())
    app.run()
