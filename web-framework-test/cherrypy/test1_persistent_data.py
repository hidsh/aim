#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cherrypy

class Hello(object):
    def __init__(self):
        self.data = 0
    
    def index(self):
        self.data += 1
        return '%d' % self.data
    index.exposed = True
    


##
if __name__ == '__main__':
    cherrypy.quickstart(Hello())


    # persistent data? YES
    # per user?        NO!!!!!!!!!!!!
    
