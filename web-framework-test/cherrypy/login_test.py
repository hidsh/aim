#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cherrypy

class Root:
    def index(self):
        return open('login_test.html', 'r').read()
    index.exposed = True

    def doLogin(self, username=None, password=None):
        if username=='foo' and password=='bar':
            return '<html><head></head><body><h1 style="color:green">Logged in!</h1></body></html>'
        else:
            return '<html><head></head><body><p style="color:red">incorrect. try again.</p><p><a href="http://localhost:8080/">Back</a></p></body></html>'
    doLogin.exposed = True


##
if __name__ == '__main__':
    cherrypy.quickstart(Root())
