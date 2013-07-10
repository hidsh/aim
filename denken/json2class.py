#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json

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

class Questions(object):
   def __init__(self, json_name):
        if os.path.exists(json_name):
            fobj = open(json_name, 'r', encoding='utf-8')
            try:
                l = json.load(fobj)
            finally:
                fobj.close()
        else:
            error('not exists:%s' % json_name)

        self.__list__ = []
        for d in l:
            q = Question(d['YEAR'], d['NUM'], d['Q'], d['OPTS'], d['A'], d['DESC'])
            self.__list__.append(q)
            
   def __iter__(self):
       for x in self.__list__:
           yield x

   def __getitem__(self, index):
       return self.__list__[index]

   def __repr__(self):
       return repr(self.__list__)

   def __len__(self):
        return len(self.__list__)

##
if __name__ == '__main__':
    ql = Questions('houki_a.json')
    
    for o in ql:
        # print("%d - %d: %s.. %s, %s, %s, %s, %s\n" %
        #       (o.ad, o.num, o.qstr[:6], o.opt_head, o.opt_type, o.opts[1], o.opts[2], o.opts[3]))
        print("%d - %d: %s.." %
              (o.ad, o.num, o.qstr[:20]))

    print(ql[4])
    # print(ql)
    print("count:%d問\n" % len(ql))

