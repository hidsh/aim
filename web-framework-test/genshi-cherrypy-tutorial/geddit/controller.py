#!/usr/bin/env python

import operator, os, pickle, sys

import cherrypy
from genshi.template import TemplateLoader
from geddit.model import Link, Comment

loader = TemplateLoader(
    os.path.join(os.path.dirname(__file__), 'templates'),
    auto_reload=True
)

class Root(object):
    def __init__(self, data):
        self.data = data

    @cherrypy.expose
    def index(self):
        links = sorted(self.data.values(), key=operator.attrgetter('time'))
        
        tmpl = loader.load('index.html')
        stream = tmpl.generate(links=links)
        return stream.render('html', doctype='html')


def main(filename):
    # load data from the pickle file, or initialize it to an empty list
    if os.path.exists(filename):
        fileobj = open(filename, 'rb')
        try:
            data = pickle.load(fileobj)
        finally:
            fileobj.close()
    else:
        data = {}

    print data

    def _save_data():
        fileobj = open(filename, 'wb')
        try:
            pickle.dump(data, fileobj)
        finally:
            fileobj.close()
            
    if hasattr(cherrypy.engine, 'subscribe'):  # cherrypy >=3.1
        cherrypy.engine.subscribe('stop', _save_data)
    else:
        cherrypy.engine.on_stop_engine_list.append(_save_data)

    # Some global configuration; note that this could be moved into a
    # configuration file
    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
    })

    cherrypy.quickstart(Root(data), '/', {
        '/media': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    })


    
if __name__ == '__main__':
    main(sys.argv[1])
