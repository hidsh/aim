# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 11:50:55 2013

@author: g
"""

from gevent.wsgi import WSGIServer
import gevent

def application(environ, start_response):
    status = '200 OK'

    headers = [
        ('Content-Type', 'text/html')
    ]

    start_response(status, headers)
    for x in range(256):
#        gevent.sleep(2)
        yield '<p style="color:#%02X7F7F">count: %03d</p>' % (x, x)
		

WSGIServer(('', 8000), application).serve_forever()
