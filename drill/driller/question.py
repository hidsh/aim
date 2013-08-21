#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, random
import configparser
from markdown import markdown
from genshi.core import Markup

from driller.model import ObjList

from driller.lib import util
from driller.lib import deco

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
    re_opt_head = re.compile(r'[ \t　]+')
    re_p     = re.compile(r'</?p>')

    def __init__(self, ad, qnum, q, opts, a, desc, history):
        def _replace_blanks(html):
            return self.re_blank.sub(r'<span class="blank">\1</span>', html)

        def _to_num(x):
            s = x.strip()
            return int(s) if s and s.isdigit() else None

        def _opt_md(x):
            m = Markup(markdown(x.replace('\\n', '\n\n'), ['tables']))
            
            return Markup(self.re_p.sub('', m))
        
        self.ad = ad
        self.nengo, self.jy = util.jpn_year(ad)
        self.qnum = qnum
        self.qstr = Markup(_replace_blanks(markdown(q, ['tables'])))

        ans = [_to_num(x) for x in a]
        self.opt_typ  = 'checkbox' if len(ans) > 1 else 'radio'

        opts = list(opts)
        opt_top = opts.pop(0).strip()
        if opt_top.startswith('-'):
            self.opt_style = 'no_head'
            self.opt_head  = None
        else:
            self.opt_style = 'with_head'
            self.opt_head  = self.re_opt_head.split(opt_top)
        
        self.opts = []
        for i,line in enumerate(opts, 1):
            cols = [_opt_md(x) for x in self.re_opt.split(line.strip())]
            hit = '*' if i in ans else None                  # '*' <-- correct answer
            self.opts.append(Option(i, hit, cols))

        self.desc = None if desc == '' else Markup(_replace_blanks(markdown(desc, ['tables'])))
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
    def __init__(self, path_txt, history_list):
        def _to_num(x):
            s = x.strip()
            return int(s) if s and s.isdigit() else None
        def _get_value(_dict,_key):
            return _dict[_key] if _key in _dict else ''
        def _is_cache_old(path_cache, path_txt):
            mod_cache = os.stat(path_cache).st_mtime
            mod_txt   = os.stat(path_txt).st_mtime
            if mod_cache < mod_txt:
                return True
            else:
                return False
            
        if not os.path.exists(path_txt):
            raise FileNotFoundError('%sがありません' % path_txt)

        path_cache = util.filename_body(path_txt) + '.cache'
        if os.path.exists(path_cache) and not _is_cache_old(path_cache, path_txt):
            self.load(path_cache)
        else:
            ini = configparser.RawConfigParser()
            ini.read(path_txt, encoding='utf-8')

            self.filename = os.path.basename(path_txt)
            l = []
            for sect in ini.sections():
                if sect == 'HEAD':
                    self.name    = _get_value(ini[sect], 'NAME')
                    self.desc    = _get_value(ini[sect], 'DESC')
                    self.authors = [x.strip() for x in _get_value(ini[sect], 'AUTHORS').split(',')]
                else:
                    ad,qnum = [_to_num(x) for x in sect.split(',')]
                    q = _get_value(ini[sect], 'Q')
                    opts = [x for x in _get_value(ini[sect], 'OPTS').split('\n') if x != '']
                    a = [x.strip() for x in _get_value(ini[sect], 'A').split(',')]
                    desc = _get_value(ini[sect], 'DESC')
                    his = [x[0] for x in history_list.get_ox_list(ad, qnum)]
                    q = Question(ad, qnum, q, opts, a, desc, his)
                    l.append(q)

            self._list = l
            self.save(path_cache)

        
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
        n_gr  = len([c for c in colors if c == Question.GREEN])
        n_ye  = len([c for c in colors if c == Question.YELLOW])
        n_re  = len([c for c in colors if c == Question.RED])
        n_wh  = len([c for c in colors if c == Question.WHITE])
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
