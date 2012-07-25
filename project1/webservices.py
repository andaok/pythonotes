# -*- encoding:utf-8 -*-

'''
Created on Jul 24, 2012

@author: root
'''

import bottle
from bottle import  route, run

'''
@route('/hello/:name')
def index(name="world"):
    return '<b>hello %s!</b>' %name

run(host='localhost',port=8080)
'''

@route('/',method='GET')
def homepage():
    return 'hello world!'

@route('/event/:id',method='GET')
def get_event(id):
    return dict(name = 'event' + str(id))

bottle.debug(True)
run(host='localhost',port=8080)





