# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 11:50:55 2013

@author: g
"""

from gevent.pywsgi import WSGIServer

def application(environ, start_response):
    status = '200 OK'

    headers = [
        ('Content-Type', 'text/html')
    ]

    start_response(status, headers)
    yield "<p>Hello"
    yield "World</p>"

WSGIServer(('', 8000), application).serve_forever()
