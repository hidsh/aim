#! /usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy
from genshi.template import MarkupTemplate
from genshi.core import Markup

template = '''
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>test</title>
  </head>
  <body>
      <div>$x1</div>
      <hr />
      <div>$x2</div>
  </body>
</html>'''

class Root(object):
    @cherrypy.expose
    def index(self):
        s = '<p><a href="example.com">come here!</a><p>'
        m = Markup(s)
        
        tmpl = MarkupTemplate(template)
        return tmpl.generate(x1=s, x2=m).render('html', doctype='html')


if __name__ == '__main__':
    cherrypy.quickstart(Root())



# [How can I include literal XML in template output?](http://genshi.edgewall.org/wiki/GenshiFaq#HowcanIincludeliteralXMLintemplateoutput)
