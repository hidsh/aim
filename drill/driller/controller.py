#!/usr/bin/env python

import operator, os, pickle, sys
from datetime import datetime

import cherrypy
from genshi.template import TemplateLoader
from genshi.filters import HTMLFormFiller

from driller.model import ExamConf, ExamResult
from driller.question import QuestionList, QuestionPages, QuestionPagesForPrint
from driller.answer import AnswerList
from driller.history import HistoryList
from driller.user import User
from driller.lib import template


class PageInfo(object):
    def __init__(self, idx, qpages, qn):
        self.idx    = idx                    # 0..
        self.page_num = idx + 1              # 1..
        self.page_max = len(qpages)
        self.qn = qn

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
        user_account = 'hoge@gmail.com'               # test
        exam_json    = 'houki_a.json'                 # test

        # cherrypy.lib.sessions.expire()

        cherrypy.session['user_mail'] = user_account
        cherrypy.session['exam_json'] = exam_json

        raise cherrypy.HTTPRedirect('exam_root')

    @cherrypy.expose
    @template.output('exam_root.html')
    def exam_root(self, **post_dict):
        assert cherrypy.session['user_mail']
        assert cherrypy.session['exam_json']

        user = User(cherrypy.session['user_mail'])
        try:
            user.load()
        except Exception as e:
            user.conf = ExamConf()
            user.history = HistoryList()
            user.save()
            print('ユーザ %s のファイルが見つかりませんでした。デフォルトの設定を保存します。: %r' % (user.mail_addr, e))

        ql = QuestionList(cherrypy.session['exam_json'], user.history)
        
        if post_dict:
            if post_dict['level_reset'] == 'yes':
                user.history.level_reset(ql)
                user.save()
                raise cherrypy.HTTPRedirect('exam_root')              # reload
        
        cherrypy.session['ql'] = ql
        user.conf.mode = 'drill'                                      # default mode
        hists = user.history.out()
        stat  = ql.get_color_distribution()
        return template.render(n=len(ql), hists=hists, stat=stat, u=user) | HTMLFormFiller(data=user.conf.to_dict())


    @cherrypy.expose
    @template.output('exam_print.html')
    def exam_print(self, **post_dict):
        assert post_dict
        assert cherrypy.session['ql']
        assert cherrypy.session['user_mail']

        ql = cherrypy.session['ql']
        qpages = QuestionPagesForPrint(ql)
        navi = [None, Navi('最初に戻る', '/')]
        pginfo = PageInfo(0, qpages, len(qpages[0]))
        user = User(cherrypy.session['user_mail'])
            
        return template.render(questions=qpages[0], navi=navi, pginfo=pginfo, u=user)
        
    @cherrypy.expose
    @template.output('exam.html')
    def exam_start(self, **post_dict):
        assert post_dict
        assert cherrypy.session['ql']
        assert cherrypy.session['user_mail']

        user = User(cherrypy.session['user_mail'])

        try:
            user.load()
        except Exception as e:
            print('ユーザ %s の設定ファイルが見つかりませんでした。デフォルトの設定でドリルを開始します。: %r' % (user.mail_addr, e))
            
        conf = ExamConf(post_dict)
        user.update_conf(conf)
        user.save()

        cherrypy.session['conf'] = user.conf
        cherrypy.session['start_time'] = datetime.now()
        
        ql = cherrypy.session['ql']
        cherrypy.session['qpages'] = qpages = QuestionPages(ql, user.conf)
        cherrypy.session['answer_dict'] = {}
        navi = [None, Navi('次ページ')]
        pginfo = PageInfo(0, qpages, user.conf.qn)

        return template.render(questions=qpages[0], navi=navi, pginfo=pginfo, u=user)

    @cherrypy.expose
    @template.output('exam.html')
    def exam(self, **post_dict):
        assert post_dict

        try:
            cmd = post_dict.pop('_cmd')
            page_num  = int(post_dict.pop('_pg'))
        except ValueError:
            print('invalid post request:post_dict=%s' % post_dict)
            raise cherrypy.HTTPRedirect('request_error')
        except Exception as e:
            print('unknown error: %r' % e)
            raise cherrypy.HTTPRedirect('unknown_error')            
        
        cherrypy.session['answer_dict'].update(post_dict)
        
        try:
            qpages = cherrypy.session['qpages']
            conf = cherrypy.session['conf']
            user = User(cherrypy.session['user_mail'])
        except cherrypy.HTTPError:
            raise cherrypy.HTTPRedirect('session_error')

        assert 0 <= page_num <= len(qpages), 'page_num:%d' % page_num

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

        pginfo = PageInfo(page_num_new, qpages, conf.qn)
        return template.render(questions=qpages[page_num_new], navi=navi, pginfo=pginfo, u=user) | HTMLFormFiller(data=cherrypy.session['answer_dict'])

    @cherrypy.expose
    @template.output('exam_finish_confirm.html')
    def exam_finish_confirm(self):
        try:
            qpages = cherrypy.session['qpages']
            user = User(cherrypy.session['user_mail'])
        except cherrypy.HTTPError:
            raise cherrypy.HTTPRedirect('session_error')
        
        page_num = len(qpages)                     # (last question page) + 1
        navi = [Navi('前ページ'), None]
        return template.render(navi=navi, pg=page_num, u=user)

    @cherrypy.expose
    @template.output('exam_result.html')
    def exam_result(self, **post_dict):
        try:
            start_time = cherrypy.session['start_time']
            qpages   = cherrypy.session['qpages']
            ans_dict = cherrypy.session['answer_dict']
            user     = User(cherrypy.session['user_mail'])
        except cherrypy.HTTPError:
            raise cherrypy.HTTPRedirect('session_error')

        try:
            user.load()
        except Exception as e:
            user.history = HistoryList()
            print('ユーザ %s のファイルが見つかりませんでした。ヒストリを新規に作ります。: %r' % (user.mail_addr, e))

        result = ExamResult(qpages[:], AnswerList(ans_dict), user.history)

        user.history.append(result.summarize(), start_time)
        user.save()
        time = user.history.get_last_time()

        result = ExamResult(qpages[:], AnswerList(ans_dict), user.get_history_old(start_time)) # for output to html

        navi = [None, Navi('最初に戻る', '/')]
        return template.render(navi=navi, score=result.get_score(), results=result, time=time, u=user)

    @cherrypy.expose
    @template.output('session_error.html')
    def session_error(self):
        try:
            user = User(cherrypy.session['user_mail'])
        except Exception as e:
            print('ユーザーのメールアドレスが不正です:%r' % e)

        return template.render(u=user)
        
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
        'tools.sessions.timeout': 60,        # 60 min
        'tools.sessions.storage_type': 'file',
        'tools.sessions.storage_path': './sessions'
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
    
