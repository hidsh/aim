#! /usr/bin/env python
# -*- coding:utf-8 -*-
import cherrypy

class Folder(object):
    def index(self):
        return 'マイフォルダ'
    index.exposed = True

class Site(object):
    def index(self):
        return '自分のサイト'
    index.exposed = True

    foo = Folder()

    def blog(self, year, month, day):
        return 'ブログ %s-%s-%s' % (year, month, day)
    blog.exposed = True

cherrypy.quickstart(Site())


# python hello.py
# http://localhost:8080/foo/             <-- Folderクラスの indexメソッドを呼び出し
# http://localhost:8080/                 <-- Siteクラスの indexメソッドを
# http://localhost:8080/blog/2013/01/08  <-- Siteクラスの blogメソッドを
