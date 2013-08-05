#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, random
import configparser
from markdown import markdown
from genshi.core import Markup

from driller.model import ObjList

from driller.lib import util

class Option(object):
    def __init__(self, num, hit, cols=[]):
        self.onum = num
        self.hit  = hit
        self.cols = cols
        self.your_ans = None

    def __repr__(self):
        return '%2d:%s:%s' % (self.onum, self.hit, self.your_ans)

class Question(object):
    GREEN  = 'green'                     # level 3
    YELLOW = 'yello'                     #       2
    RED    = 'red'                       #       1
    WHITE  = 'white'                     #       0
    re_blank = re.compile(r'\[{2}(.)\]{2}')            # e.g. [[ア]] --> ア
    re_opt   = re.compile(r'[ \t　]{2,}')

    def __init__(self, ad, qnum, q, opts, a, desc, history):
        def _replace_blanks(html):
            return self.re_blank.sub(r'<span class="blank">\1</span>', html)

        def _to_num(x):
            s = x.strip()
            return int(s) if s and s.isdigit() else None
        
        self.ad = ad
        self.nengo, self.jy = util.jpn_year(ad)
        self.qnum = qnum
        self.qstr = Markup(_replace_blanks(markdown(q, ['tables'])))

        ans = list(map(_to_num, a))
        self.opt_typ  = 'checkbox' if len(ans) > 1 else 'radio'

        opts = list(opts)
        opt_top = opts.pop(0).strip()
        if opt_top.startswith('-'):
            self.opt_style = 'no_head'
            self.opt_head  = None
        else:
            self.opt_style = 'with_head'
            self.opt_head  = self.re_opt.split(opt_top)
        
        self.opts = []
        for i,line in enumerate(opts, 1):
            cols = self.re_opt.split(line.strip())
            hit = '*' if i in ans else None                  # '*' <-- correct answer
            self.opts.append(Option(i, hit, cols))

        self.desc = None if desc == '' else desc
        self.history = history

    def get_color(self, by):             # by: 'color'|'level'
        if   self.history == [] or self.history[0] == 'reset':
            color = self.WHITE
            level = 0
        elif self.history[0:2] == ['correct', 'correct']:
            color = self.GREEN
            level = 3
        elif self.history[0] == 'correct':
            color = self.YELLOW
            level = 2
        else:
            color = self.RED
            level = 1

        if by == 'color':
            return color
        else:
            return level

    def correct_answer(self):
        return [x.onum for x in filter(lambda x: x.hit=='*', self.opts)]


class QuestionList(ObjList):
    def __init__(self, path, history_list):
        def _to_num(x):
            s = x.strip()
            return int(s) if s and s.isdigit() else None
        def _get_value(_dict,_key):
            return _dict[_key] if _key in _dict else ''
            

        if not os.path.exists(path):
            raise FileNotFoundError('%sがありません' % path)

        ini = configparser.RawConfigParser()
        ini.read(path, encoding='utf-8')

        l = []
        for sect in ini.sections():
            ad,qnum = map(lambda x: _to_num(x), sect.split(','))
            q = _get_value(ini[sect], 'Q')
            opts = filter(lambda x: x != '', _get_value(ini[sect], 'OPTS').split('\n'))
            a = map(lambda x: x.strip(), _get_value(ini[sect], 'A').split(','))
            desc = _get_value(ini[sect], 'DESC')
            his = list(map(lambda x: x[0], history_list.get_answer_list(ad, qnum)))
            q = Question(ad, qnum, q, opts, a, desc, his)
            l.append(q)

        self._list = l

    def sort_by_poor_questions(self):
        l = self._list[:]
        for x in l:
            x.level = x.get_color('level')
            
        l.sort(key=lambda x:x.level)
        for x in l:
            delattr(x, 'level')
        return l
        
    def get_color_distribution(self):
        colors = [x.get_color('color') for x in self._list]
        n     = len(colors)
        n_gr  = len(list(filter(lambda c: c == Question.GREEN,  colors)))
        n_ye  = len(list(filter(lambda c: c == Question.YELLOW, colors)))
        n_re  = len(list(filter(lambda c: c == Question.RED,    colors)))
        n_wh  = len(list(filter(lambda c: c == Question.WHITE,  colors)))
        # TODO: adjust max value ratio
        
        return ((n, 100), (n_gr, util.percent(n_gr, n)), (n_ye, util.percent(n_ye, n)), (n_re, util.percent(n_re, n)), (n_wh, util.percent(n_wh, n)))


class QuestionPages(ObjList):
    def __init__(self, ql, conf):
        qlx = ql[:]
        if conf.order == 'poor':         # poor | cont | random
            random.shuffle(qlx)
            qlx = ql.sort_by_poor_questions()
            
        elif conf.order == 'rand':
            random.shuffle(qlx)

        selected = qlx[:conf.qn]
        
        for i,q in enumerate(selected, 1):
            q.i = i                      # question number
            random.shuffle(q.opts)

        self._list = util.split_seq(selected, conf.n_per_page)


class QuestionPagesForPrint(ObjList):
    def __init__(self, ql):
        qlx = ql[:]
        
        for i,q in enumerate(qlx, 1):
            q.i = i                      # question number

        self._list = [qlx]

         
##
if __name__ == '__main__':
    
    ql = QuestionList('../questions/houki_a/houki_a.txt')
    
    for o in ql[:3]:
        print("%d - %2d: %s.." % (o.ad, o.qnum, o.qstr[:20]))

    o = ql[10]
    print("%d - %2d: %s.. %s, %s, %s, %s, %s\n" %
          (o.ad, o.qnum, o.qstr[:6], o.opt_head, o.opt_typ, o.opts[1], o.opts[2], o.opts[3]))

    print("count:%d問\n" % len(ql))

    ####

    print('-' * 20)
    from model import ExamConf
    conf = ExamConf(n=13, method=['random'], n_per_page=5)

    qp = QuestionPages(ql, conf)
    for i,p in enumerate(qp):
        print('-- page: %d --' % i)
        for o in p:
            print("%d - %2d: %s.." % (o.ad, o.qnum, o.qstr[:20]))
    
    print('-' * 20)
    qs = qp[1]
    for o in qs:
        print("%d - %2d: %s.." % (o.ad, o.qnum, o.qstr[:20]))

    print('--- original ql not broken?')
    for o in ql[:3]:
        print("%d - %2d: %s.." % (o.ad, o.qnum, o.qstr[:20]))
