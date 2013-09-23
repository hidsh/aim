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
    re_blank = re.compile(r'\[{2}(.)\]{2}')            # e.g. [[ア]] --> ア
    re_opt   = re.compile(r'[ \t　]{2,}')
    re_opt_head = re.compile(r'[ \t　]+')
    re_p     = re.compile(r'</?p>')

    def __init__(self, ad, qnum, q, opts, a, desc):
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

    def correct_answer(self):
        return [x.onum for x in filter(lambda x: x.hit=='*', self.opts)]


class QuestionList(ObjList):
    def __init__(self, path_txt):
        def _to_num(x):
            s = x.strip()
            return int(s) if s and s.isdigit() else None
        
        def _get_value(_dict,_key):
            return _dict[_key] if _key in _dict else ''

        def _is_cache_old(path_cache, path_txt):
            mod_cache = os.stat(path_cache).st_mtime
            mod_txt   = os.stat(path_txt).st_mtime
            return mod_cache < mod_txt
            
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
                    q = Question(ad, qnum, q, opts, a, desc)
                    l.append(q)

            self._list = l
            self.save(path_cache)

    def sort_by_poor_questions(self, color_dists):
        def _lv_str2num(lv_str):
            tbl = {'lv_re':0, 'lv_ye':2, 'lv_gr':3 }
            return tbl[lv_str]
            
        ql = self._list[:]
        [setattr(q,'level', _lv_str2num(c['lv_xx'])) for c,q in zip(color_dists, ql)]
            
        ql.sort(key=lambda x:x.level)
        [delattr(q, 'level') for q in ql]
        return ql
    
class QuestionPages(ObjList):
    def __init__(self, ql, conf, color_dists):
        qlx = ql[:]
        # import pdb; pdb.set_trace()

        random.seed()
        if conf.order == 'poor':         # poor | cont | rand
            random.shuffle(qlx)
            qlx = ql.sort_by_poor_questions(color_dists)
            
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
