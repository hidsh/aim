#!/usr/bin/env python

import operator, os, pickle, sys

import cherrypy
from genshi.template import TemplateLoader

from driller.model import ExamConf, ExamResult
from driller.question import QuestionList, QuestionPages
from driller.answer import AnswerList
from driller.lib import template


class PageInfo(object):
    def __init__(self, index, qpages, qn):
        self.index    = index                  # 0..
        self.page_num = index + 1              # 1..
        self.page_max = len(qpages)
        self.qnum_all = qn

class Navi(object):
    def __init__(self, label, dispatcher='exam'):
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
        cherrypy.session['qpages'] = qpages = QuestionPages(ql, conf)
        cherrypy.session['answer_dict'] = {}

        navi = [None, Navi('次ページ')]
        page_num = 0
        pginfo = PageInfo(page_num, qpages, conf.n)
        return template.render(questions=qpages[page_num], navi=navi, pginfo=pginfo)

    @cherrypy.expose
    @template.output('exam.html')
    def exam(self, **post_dict):
        assert post_dict

        try:
            cmd = post_dict.pop('_cmd')
            page_num  = int(post_dict.pop('_pg'))
        except ValueError:
            raise ValueError('ページ番号が変です')
        except:
            raise Error('Unknown Errror')
        
        cherrypy.session['answer_dict'].update(post_dict)
        
        try:
            qpages = cherrypy.session['qpages']
        except cherrypy.HTTPError:
            raise cherrypy.HTTPRedirect('session_error')

        assert 0 <= page_num <= len(qpages) - 1

        if cmd == 'prev':
            assert 1 <= page_num

            page_num_new = page_num - 1

            if page_num_new == 0:
                navi = [None,            Navi('次ページ')]
            else:
                navi = [Navi('前ページ'), Navi('次ページ')]
        elif cmd == 'next':
            assert page_num <= len(qpages) - 1
            
            page_num_new = page_num + 1
            
            if page_num_new == len(qpages):
                raise cherrypy.HTTPRedirect('exam_finish_confirm')

            if page_num_new == len(qpages) - 1:
                navi = [Navi('前ページ'), Navi('テスト終了', 'exam_finish_confirm')]
            else:
                navi = [Navi('前ページ'), Navi('次ページ')]

        pginfo = PageInfo(page_num_new, qpages, cherrypy.session['conf'].n)
        return template.render(questions=qpages[page_num_new], navi=navi, pginfo=pginfo)

    @cherrypy.expose
    @template.output('exam_finish_confirm.html')
    def exam_finish_confirm(self):
        try:
            qpages = cherrypy.session['qpages']
        except cherrypy.HTTPError:
            raise cherrypy.HTTPRedirect('session_error')
        
        page_num = len(qpages) - 2                     # last question page
        navi = [Navi('前ページ'), None]
        return template.render(navi=navi, pg=page_num)

    @cherrypy.expose
    @template.output('session_error.html')
    def session_error(self):
        return template.render()

    @cherrypy.expose
    @template.output('exam_result.html')
    def exam_result(self, **post_dict):
        try:
            qpages   = cherrypy.session['qpages']
            ans_dict = cherrypy.session['answer_dict']
        except cherrypy.HTTPError:
            raise cherrypy.HTTPRedirect('session_error')

        # qpages.save()
        result = ExamResult(qpages[:], AnswerList(ans_dict))
        navi = [None, Navi('最初に戻る', '/')]
        return template.render(navi=navi, score=result.get_score(), results=result)

        
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
        'tools.sessions.timeout': 60        # 60 min
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
    
