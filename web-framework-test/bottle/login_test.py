#! /usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import route, post, request, run, template


@route('/login')
def login():
    return template('login_test')
    
@post('/doLogin')
def doLogin():
    name = request.forms.get('username')
    password = request.forms.get('password')
    print(name,password)
    if name=='foo' and password=='bar':
        count = 1
        out = template('login_succeeded', name=name, i=count)
    else:
        out = template('login_failed')
    return out

run(host='localhost', port=8080, debug=True, reloader=True)

# $python ./hello.py
# http://localhost:8080/hello

