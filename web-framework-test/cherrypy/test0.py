#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cherrypy

class Hello:
    def index(self):
        return 'Hello'
    index.exposed = True
    


##
if __name__ == '__main__':
    cherrypy.quickstart(Hello())
