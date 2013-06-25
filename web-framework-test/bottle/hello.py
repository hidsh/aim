#! /usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import route,run

@route('/hello')
def hello():
    return 'こんにちわ世界!'

run(host='localhost', port=8080, debug=True)

# $python ./hello.py
# http://localhost:8080/hello
