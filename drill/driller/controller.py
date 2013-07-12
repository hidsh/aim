#!/usr/bin/env python

import operator, os, pickle, sys

import cherrypy
from genshi.template import TemplateLoader

from driller.model import ExamAnswer, ExamConf
from driller.question import QuestionList, QuestionPages
from driller.lib import template

loader = TemplateLoader(
    os.path.join(os.path.dirname(__file__), 'templates'),
    auto_reload=True
)

class PageInfo(object):
    def __init__(self, index, qpages):
        self.page_num = index
        self.page_max = len(qpages) - 1

class Navi(object):
    def __init__(self, label, dispatcher="exam"):
        self.label = label
        self.dispatcher = dispatcher
        
class Root(object):
    def __init__(self, data):
        self.data = data

    @cherrypy.expose
    @template.output('index.html')
    def index(self):
        return template.render(title='電気ドリル')

    @cherrypy.expose
    @template.output('exam.html')
    def exam_start(self):
        cherrypy.session['conf'] = ExamConf(n=7, method=['seq'], n_per_page=2) # test (set from previous page)

        conf = cherrypy.session['conf']                  # test (get from prev page)
        ql = QuestionList('houki_a.json')
        qpages = cherrypy.session['qpages'] = QuestionPages(ql, conf)

        navi = [None, Navi("次ページ")]
        pginfo = PageInfo(1, qpages)
        return template.render(questions=qpages[1], navi=navi, pginfo=pginfo)

    @cherrypy.expose
    @template.output('exam.html')
    def exam(self, pg, cmd):
        page_num = int(pg)
        cmd = cmd
        
        qpages = cherrypy.session['qpages']

        assert 1 <= page_num <= len(qpages) - 1

        if cmd == 'prev':
            assert 2 <= page_num

            page_num_new = page_num - 1

            if 1 < page_num_new:
                navi = [Navi("前ページ"), Navi("次ページ")]
            else:
                navi = [None, Navi("次ページ")]
        elif cmd == 'next':
            assert page_num <= len(qpages) - 2
            
            page_num_new = page_num + 1
            
            if page_num_new < len(qpages) - 1:
                navi = [Navi("前ページ"), Navi("次ページ")]
            else:
                navi = [Navi("前ページ"), Navi("テスト終了", "exam_finish_confirm")]

        pginfo = PageInfo(page_num_new, qpages)
        return template.render(questions=qpages[page_num_new], navi=navi, pginfo=pginfo)

    @cherrypy.expose
    @template.output('exam_finish_confirm.html')
    def exam_finish_confirm(self):
        qpages = cherrypy.session['qpages']

        navi = [Navi("前ページ"), None]
        return template.render(questions=qpages[page_num], navi=navi)

        
        
    
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

        'tools.sessions.on': True,
        'tools.sessions.timeout': 60,        
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
    
