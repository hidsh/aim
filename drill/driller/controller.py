#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from driller.lib import util

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
    app_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')
    
    def __init__(self):
        pass
 
    @cherrypy.expose
    @template.output('index.html')
    def index(self):
        user_id = '__g'                              # test
        q_path  = 'houki_a.txt'                      # test

        # image directory for each questions
        cherrypy.request.app.merge( config={
                '/img': {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': '../questions/%s/img' % util.filename_body(q_path)
                }
        })
        qdir = os.path.join(cherrypy.config['tools.staticdir.root'],
                            os.path.dirname(cherrypy.request.app.config['/img']['tools.staticdir.dir']))
        
        cherrypy.session['q_path']  = os.path.join(qdir, q_path)
        cherrypy.session['user_id'] = user_id

        raise cherrypy.HTTPRedirect('exam_root')

    @cherrypy.expose
    @template.output('exam_root.html')
    def exam_root(self, **post_dict):
        try:
            user_id = cherrypy.session['user_id']
            q_path  = cherrypy.session['q_path']
        except KeyError:
            raise cherrypy.HTTPRedirect('session_error')
            
        ql = QuestionList(q_path)
        user = User(user_id)
        try:
            user.load()
        except Exception as e:
            print('ユーザ %s のファイルが見つかりませんでした。デフォルトの設定を保存します。:%r' % (user.mail_addr, e))
            user.conf = ExamConf()
            user.history = HistoryList(ql)
            user.save()
        
        if post_dict and post_dict['level_reset'] == 'yes':
            user.history.level_reset(ql)
            user.save()
            raise cherrypy.HTTPRedirect('exam_root')              # reload
        
        cherrypy.session['ql'] = ql
        a = user.id in ql.authors
        about = {'filename':ql.filename, 'name':ql.name, 'desc':ql.desc, 'authors':ql.authors, 'n':len(ql)}
        user.conf.mode = 'drill'                                      # default mode
        hists = user.history.out()
        stat  = user.history.get_color_distribution()
        hist_chart = user.history.get_history_chart()
        return template.render(about=about, hists=hists, stat=stat, h_chart = hist_chart, u=user, author=a) | HTMLFormFiller(data=user.conf.to_dict())


    @cherrypy.expose
    @template.output('exam_print.html')
    def exam_print(self, **post_dict):
        assert post_dict
        try:
            ql       = cherrypy.session['ql']
            user_id  = cherrypy.session['user_id']
        except KeyError:
            raise cherrypy.HTTPRedirect('session_error')

        qpages = QuestionPagesForPrint(ql)
        navi = [None, Navi('最初に戻る', '/')]
        pginfo = PageInfo(0, qpages, len(qpages[0]))
        user = User(user_id)
            
        return template.render(questions=qpages[0], navi=navi, pginfo=pginfo, u=user)
        
    @cherrypy.expose
    @template.output('exam.html')
    def exam_start(self, **post_dict):
        assert post_dict
        try:
            ql       = cherrypy.session['ql']
            user_id  = cherrypy.session['user_id']
        except KeyError:
            raise cherrypy.HTTPRedirect('session_error')

        user = User(user_id)

        try:
            user.load()
        except Exception as e:
            print('ユーザ %s の設定ファイルが見つかりませんでした。デフォルトの設定でドリルを開始します。: %r' % (user.mail_addr, e))
            
        conf = ExamConf(post_dict)
        user.update_conf(conf)
        user.save()

        cherrypy.session['conf'] = user.conf
        cherrypy.session['start_time'] = datetime.now()
        
        cherrypy.session['qpages'] = qpages = QuestionPages(ql, user.conf, user.history.color_dists)
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
        
        try:
            _ = cherrypy.session['answer_dict']
            qpages  = cherrypy.session['qpages']
            conf    = cherrypy.session['conf']
            user_id = cherrypy.session['user_id']
        except KeyError:
            raise cherrypy.HTTPRedirect('session_error')

        cherrypy.session['answer_dict'].update(post_dict)
        
        # assert 0 <= page_num <= len(qpages), 'page_num:%d' % page_num

        if cmd == 'prev':
            # assert 1 <= page_num

            page_num_new = page_num - 1

            if page_num_new == 0:
                navi = [None,            Navi('次ページ')]
            else:
                navi = [Navi('前ページ'), Navi('次ページ')]
        elif cmd == 'next':
            # assert page_num <= len(qpages) - 1
            
            page_num_new = page_num + 1
            
            if page_num_new == len(qpages):
                raise cherrypy.HTTPRedirect('exam_finish_confirm')

            if page_num_new == len(qpages) - 1:
                navi = [Navi('前ページ'), Navi('テスト終了', 'exam_finish_confirm')]
            else:
                navi = [Navi('前ページ'), Navi('次ページ')]

        pginfo = PageInfo(page_num_new, qpages, conf.qn)
        return template.render(questions=qpages[page_num_new], navi=navi, pginfo=pginfo, u=User(user_id)) | HTMLFormFiller(data=cherrypy.session['answer_dict'])

    @cherrypy.expose
    @template.output('exam_finish_confirm.html')
    def exam_finish_confirm(self):
        try:
            qpages  = cherrypy.session['qpages']
            user_id = cherrypy.session['user_id']
        except KeyError:
            raise cherrypy.HTTPRedirect('session_error')
        
        page_num = len(qpages)                     # (last question page) + 1
        navi = [Navi('前ページ'), None]
        return template.render(navi=navi, pg=page_num, u=User(user_id))

    @cherrypy.expose
    @template.output('exam_result.html')
    def exam_result(self, **post_dict):
        try:
            start_time = cherrypy.session['start_time']
            qpages   = cherrypy.session['qpages']
            ans_dict = cherrypy.session['answer_dict']
            user     = User(cherrypy.session['user_id'])
        except KeyError:
            raise cherrypy.HTTPRedirect('session_error')

        try:
            user.load()
        except Exception as e:
            user.history = HistoryList()
            print('ユーザ %s のファイルが見つかりませんでした。ヒストリを新規に作ります。: %r' % (user.mail_addr, e))

        results = ExamResult(qpages, AnswerList(ans_dict), user.history, start_time)

        user.history.append(results, start_time)
        user.save()
        time = user.history[-1].get_time()
        score = user.history[-1].get_score()

        navi = [None, Navi('最初に戻る', '/')]
        return template.render(navi=navi, score=score, results=results, time=time, u=user)

    @cherrypy.expose
    @template.output('error.html')
    def session_error(self):
        msg = 'セッションエラーが発生しました。'
        return template.render(msg=msg)

    @cherrypy.expose
    @template.output('error.html')
    def request_error(self):
        msg = 'リクエストエラーが発生しました。'
        return template.render(msg=msg)

    @cherrypy.expose
    @template.output('error.html')
    def unknown_error(self):
        msg = '予期せぬエラーが発生しました。'
        return template.render(u=user, msg=msg)

    
def main(db_name):
    # Some global configuration; note that this could be moved into a
    # configuration file
    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),

        'tools.sessions.on': True,
        'tools.sessions.timeout': 60,        # 60: 60 min
        'tools.sessions.storage_type': 'file',
        'tools.sessions.storage_path': './sessions'
        })

    cherrypy.quickstart(Root(), '/', {
        '/media': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    })

if __name__ == '__main__':
    main('driller.db')

# $ PYTHONPATH=. python driller/controller.py
    
