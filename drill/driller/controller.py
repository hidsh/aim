#!/usr/bin/env python

import operator, os, pickle, sys

import cherrypy
from genshi.template import TemplateLoader

from driller.model import ExamAnswer, ExamConf

loader = TemplateLoader(
    os.path.join(os.path.dirname(__file__), 'templates'),
    auto_reload=True
)



class Root(object):
    def __init__(self, data):
        self.data = data
        self.udat = {}          # <------------------------------------ TODO

    @cherrypy.expose
    def index(self):
        tmpl = loader.load('index.html')
        return tmpl.generate(title='Dr.Driller').render('html', doctype='html')

    @cherrypy.expose
    def exam_start(self):
        ql = QuestionList()
        conf = ExamConf(n=7, method=['seq'], n_per_page=2) # test
        qpages = QuestionPages(ql, conf)
        for i,p in enumerate(qp):


        tmpl = loader.load('exam.html')
        return tmpl.generate(questions=questions).render('html', doctype='html')
    
def main(db_name):
    # load data from the pickle file, or initialize it to an empty list
    if os.path.exists(db_name):
        fileobj = open(db_name, 'rb')
        try:
            data = pickle.load(fileobj)
        finally:
            fileobj.close()
    else:
        data = {}

    def _save_data():
        # save data back to the pickle file
        fileobj = open(db_name, 'wb')
        try:
            pickle.dump(data, fileobj)
        finally:
            fileobj.close()
    if hasattr(cherrypy.engine, 'subscribe'): # CherryPy >= 3.1
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
    main('driller.db')

# $ PYTHONPATH=. python driller/controller.py
    
