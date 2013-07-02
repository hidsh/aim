#! /usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import route, run, template

@route('/')
@route('/hello')
@route('/hello/<name>')

def hello(name='知らない人'):
    return template('template_test_1', name=name)

run(host='localhost', port=8080, debug=True, reloader=True)

# $python ./hello.py
# http://localhost:8080/hello

