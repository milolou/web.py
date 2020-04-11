import web
import json
import datetime
from main import collection
from datetime import *
from bson.objectid import ObjectId
from main import render

class CjsonEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,datetime):
            return obj.strftime('%Y-%m-%d %H-%M-%S')
        elif isinstance(obj,date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self,obj)

def formatField(data):
    data['_id'] = str(data['_id'])
    data['post_date'] = eval(json.dumps(data['post_date'],cls=CjsonEncoder))
    return data

class TD(object):
    def GET(self):
        i = web.input()
        print(i)
        page = int(i.get('page',1))
        limit = int(i.get('limit',10))
        skip_num = (page - 1)*10
        results = []
        for post_data in collection.find().skip(skip_num).limit(limit):
            format_data = formatField(post_data)
            results.append(format_data)
        #web.header('Content-Type','application/json')
        #return json.dumps(results)
        return render.index(results)

    def POST(self):
        i = web.input()
        print i
        title = i.get('title',None)
        if not title:
            #return json.dumps({'errors':'标题让你吃了吗？'})
            return render.error('标题让你吃了吗？','/')

        post_data = {
            'title':title,
            'post_date':datetime.datetime.now()
        }
        collection.insert_one(post_data)
        format_data = formatField(post_data)
        web.header('Content-Type','application/json')
        return json.dumps(format_data)

def get_by_id(id):
    s = collection.find_one({'_id':ObjectId(id)})
    if not s:
        return False
    return s

class TD_Simple(object):
    def GET(self,id):
        todo = get_by_id(id)
        if not todo:
            #return json.dumps({'error':'没找到这条记录'})
            return render.error('没找到这条记录','/')
        format_data = formatField(todo)
        #web.header('Content-Type','application/json')
        #return json.dumps(format_data)
        return render.edit(todo)

    def PATCH(self,id):
        web.header('Content-Type','application/json')
        todo = get_by_id(id)
        if not todo:
            return json.dumps({'error':'没找到这条记录'})
        i = web.input()
        print(i)
        title = i.get('title',None)
        status = i.get('finished',None)
        if title:
            collection.update({'_id':ObjectId(id)},{"$set":{'title':title}})
        if status:
            if status.lower() == 'yes':
                finished = True
            elif status.lower() == 'no':
                finished = False
            collection.update({'_id':ObjectId(id)},{"$set":{'finished':finished}})
        if not title and not status:
            #return json.dumps({'error':'您发起了一个不允许的请求'})
            return render.error('您发起了一个不允许的请求','/')
        todo = get_by_id(id)
        format_data = formatField(todo)
        return json.dumps(format_data)

    def DELETE(self,id):
        web.header('Content-Type','application/json')
        if len(id) != 24:
            return json.dumps({'error':'id lenght is error'})
        todo = get_by_id(id)
        if not todo:
            #return json.dumps({'error':'没找到这条记录'})
            return render.error('没找到这条记录','/')
        collection.remove({'_id':ObjectId(id)})
        return json.dumps({})
