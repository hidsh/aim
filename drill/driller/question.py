#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, random
import json
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
    def __init__(self, year, num, q, opts, a, desc=''):
        def _normalize_cr(md):
            return re.sub(r'(\n)+', r'\n\n', md)
    
        def _replace_blanks(html):
            return re.sub(r'\[(.)\]', r'<span class="blank">\1</span>', html)
        
        self.ad = year
        self.nengo, self.jy = util.jpn_year(year)
        self.qnum = num
        self.qstr = Markup(_replace_blanks(markdown(_normalize_cr(q), ['tables'])))

        ans = a if type(a) is list else [a]
        self.opt_typ = 'checkbox' if len(ans) > 1 else 'radio'

        self.opts = []
        for i,line in enumerate(opts):
            cols = re.split('[ \t　]{2,}', line.strip())
            if i < 1:
                if cols == ['']:
                    self.opt_head = None
                    self.opt_style = 'no_head'
                else: 
                    self.opt_head = cols
                    self.opt_style = 'with_head'
            else:
                hit = '*' if i in ans else None                  # '*' <-- correct answer
                self.opts.append(Option(i, hit, cols))

        self.desc = None if desc == '' else desc

    def correct_answer(self):
        return [x.onum for x in filter(lambda x: x.hit=='*', self.opts)]


class QuestionList(ObjList):
    def __init__(self, json_name):
        assert os.path.exists(json_name)

        fobj = open(json_name, 'r', encoding='utf-8')
        try:
            jl = json.load(fobj)
        finally:
            fobj.close()

        l = []
        for d in jl:
            q = Question(d['YEAR'], d['NUM'], d['Q'], d['OPTS'], d['A'], d['DESC'])
            l.append(q)
        self._list = l

        
class QuestionPages(ObjList):
    def __init__(self, ql, conf):
        qlx = ql[:]
        if conf.flavor == 'ng':          # ng | random
            pass                         # TODO
            
        if conf.order == 'random':       # seq | random
            random.shuffle(qlx)

        selected = qlx[:conf.qn]
        
        for i,q in enumerate(selected, 1):
            q.i = i                      # question number
            random.shuffle(q.opts)

        self._list = util.split_seq(selected, conf.n_per_page)

        
class QuestionPagesForCheck(ObjList):
    def __init__(self, qul):
        qul = copy.deepcopy(qul)
        
        for i,q in enumerate(qul, 1):
            q.i = i                      # question number

        self._list = util.split_seq(selected, conf.n_per_page)

            
##
if __name__ == '__main__':
    
    ql = QuestionList('../houki_a.json')
    
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
