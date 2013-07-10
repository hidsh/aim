#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, random, copy
import json

import util

class Question(object):
    def __init__(self, year, num, q, opts, a, desc=''):
        self.ad = year
        self.num = num
        self.qstr = q

        ans = a if type(a) is list else [a]
        self.opt_type = 'checkbox' if len(ans) > 1 else 'radio'

        self.opts = []
        for i,line in enumerate(opts):
            cols = re.split('[ \t　]{2,}', line.strip())
            if i < 1:
                self.opt_head = None if cols == [''] else cols
            else:
                hit = '*' if i in ans else None
                self.opts.append([hit] + cols)
                
        self.desc = None if desc == '' else desc

        
class ObjList(object):
    def __init__(self):
        self.__list__ = []
    
    def __iter__(self):
        for x in self.__list__:
            yield x

    def __getitem__(self, index):
        return self.__list__[index]

    def __setitem__(self, index, value):
        self.__list__[index] = value

    def __repr__(self):
        return repr(self.__list__)

    def __len__(self):
        return len(self.__list__)

    
class QuestionList(ObjList):
    def __init__(self, json_name):
        assert os.path.exists(json_name)

        fobj = open(json_name, 'r', encoding='utf-8')
        try:
            l = json.load(fobj)
        finally:
            fobj.close()

        self.__list__ = []
        for d in l:
            q = Question(d['YEAR'], d['NUM'], d['Q'], d['OPTS'], d['A'], d['DESC'])
            self.__list__.append(q)
            

class QuestionPages(ObjList):
    def __init__(self, qul, conf):
        qul = copy.deepcopy(qul)
        if 'random' in conf.method:
            random.shuffle(qul)

        selected = qul[:conf.n]

        self.__list__ = util.split_seq(selected, conf.n_per_page)



            
##
if __name__ == '__main__':
    
    ql = QuestionList('../houki_a.json')
    
    for o in ql[:3]:
        print("%d - %2d: %s.." % (o.ad, o.num, o.qstr[:20]))

    o = ql[10]
    print("%d - %2d: %s.. %s, %s, %s, %s, %s\n" %
          (o.ad, o.num, o.qstr[:6], o.opt_head, o.opt_type, o.opts[1], o.opts[2], o.opts[3]))

    print("count:%d問\n" % len(ql))

    ####

    print('-' * 20)
    from model import ExamConf
    conf = ExamConf(n=13, method=['random'], n_per_page=5)

    qp = QuestionPages(ql, conf)
    for i,p in enumerate(qp):
        print('-- page: %d --' % i)
        for o in p:
            print("%d - %2d: %s.." % (o.ad, o.num, o.qstr[:20]))
    
    print('-' * 20)
    qs = qp[1]
    for o in qs:
        print("%d - %2d: %s.." % (o.ad, o.num, o.qstr[:20]))

    print('--- original ql not broken?')
    for o in ql[:3]:
        print("%d - %2d: %s.." % (o.ad, o.num, o.qstr[:20]))
