#! /usr/bin/env python
# -*- coding: utf-8 -*-

from genshi.core import Markup
from driller.lib import util
import pickle


class ObjList(object):
    def __init__(self):
        self._list = []
    
    def __iter__(self):
        for x in self._list:
            yield x

    def __getitem__(self, idx):
        return self._list[idx]

    def __setitem__(self, idx, value):
        self._list[idx] = value

    def __repr__(self):
        return repr(self._list)

    def __len__(self):
        return len(self._list)

    def save(self, _path):
        try:
            with open(_path, 'wb') as f:
                pickle.dump(self.__dict__, f)
        except IOError:
            print('オブジェクトを保存できませんでした: %s' % _path)
            
    def load(self, _path):
        try:
            with open(_path, 'rb') as f:
                self.__dict__ = pickle.load(f)
        except IOError:
            print('オブジェクトをロードできませんでした: %s' % _path)


class ExamConf(object):
    def __init__(self, post_dict=None):
        if post_dict:
            assert type(int(post_dict['qn']))
            assert type(int(post_dict['n_per_page']))

            self.mode   = post_dict['mode']
            self.qn     = int(post_dict['qn'])
            self.order  = post_dict['order']
            # self.tags   = post_dict['tags'] TODO
            self.tags   = [None]
            self.n_per_page = int(post_dict['n_per_page'])
        else:
            self.mode   = 'drill'     # TODO 既存のユーザ設定ファイルにメンバがないとき
            self.qn     = 3           # 'ExamConf' object has no attribute 'mode' とかになるのを
            self.order  = 'rand'      # なんとかする
            self.tags   = [None]      # なかったら、デフォルト値でメンバを差しこむ、としたい
            self.n_per_page = 2

    def __eq__(self, obj):      # TODO メンバすべてをチェック→汎化
        if obj == None:
            return False
        else:
            return (self.mode == obj.mode) and (self.qn == obj.qn) and (self.order == obj.order) and (self.n_per_page == obj.n_per_page)

    def __repr__(self):         # TODO メンバすべてをプリント→汎化
        return '<ExamConf mode:%s, qn:%d, order:%s, tags:%r, n_per_page:%d>' % (self.mode, self.qn, self.order, self.tags, self.n_per_page)

    def to_dict(self):          # TODO メンバすべてを辞書に→汎化
        return {'mode':self.mode, 'qn':self.qn, 'order':self.order, 'n_per_page':self.n_per_page}


class Result(object):
    MARU  = Markup('&#9711;')
    BATSU = Markup('&#10005;')

    def __init__(self, i, q, your_ans, hist_list):
        def _subst_mark(x):
            return self.MARU if x == 'correct' else self.BATSU
        
        def _get_color_class(now, prev):
            if [now, prev] == ['correct', 'correct']:
                return 'lv_gr'
            elif now == 'correct':
                return 'lv_ye'
            else:
                return 'lv_re'

        self.i = i

        correct_ans = q.correct_answer()
        if set(correct_ans) == set(your_ans):
            self.typ_str = self.MARU
            self.typ_class = 'correct'
        else:
            self.typ_str = self.BATSU
            self.typ_class = 'wrong'
        
        opts = []
        for qo in q.opts:
            o = qo
            o.your_ans = '+' if o.onum in your_ans else None
            opts.append(o)
            
        self.q = q
        self.q.opts = opts

        self.history = [_subst_mark(x) for x in hist_list]
        h = hist_list[0] if len(hist_list) > 0 else 'reset'
        self.lv_xx = _get_color_class(self.typ_class, h)
        
    def is_correct(self):
        return self.typ_class == 'correct'


class ExamResult(ObjList):
    def __init__(self, qpages, ans_list, history, start_time):
        h = history.get_previous(start_time)             # prevent new history when reload
        hist_limit = 10
        l = []
        for i,(q,a) in enumerate(zip(util.flatten(qpages), ans_list), 1):
            # assert i == q.i == a.i
            hist_list = [x[0] for x in h.get_ox_list(q.ad, q.qnum)][:hist_limit]
            l.append(Result(i, q, a.ans, hist_list))
        self._list = l

    def get_score(self):        # TODO refactoring: History's same function
        correct_answers = [x for x in self._list if x.is_correct()]
        len_all  = len(self._list)
        len_corr = len(correct_answers)
        percent = util.percent(len_corr, len_all)
        
        return (len_corr, len_all, percent)

    
##
if __name__ == '__main__':

    from driller.question import QuestionList, QuestionPages
    from driller.answer import AnswerList

    ExamConf(n=7, method=['seq'], n_per_page=2) # test (set from previous page)
    ql = QuestionList('houki_a.json')
    qpages = QuestionPages(ql, conf)
    # ans_dict = 
    result = ExamResult(qpages[:], AnswerList(ans_dict))

    for i,x in range(10):
        pass
