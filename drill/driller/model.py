#! /usr/bin/env python
# -*- coding: utf-8 -*-

from genshi.core import Markup
from driller.lib import util


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

    def save(self, path='./hoge.dat'):
        import pickle
        try:
            f = open(path, 'wb')
            pickle.dump(self._list, f, 2)
        except:
            print('can\'t save pickled data to %s' % path)
        finally:
            f.close()


class ExamConf(object):
    def __init__(self, post_dict=None):
        if post_dict:
            assert type(int(post_dict['qn']))
            assert type(int(post_dict['n_per_page']))

            self.mode   = post_dict['mode']
            self.qn     = int(post_dict['qn'])
            self.order  = post_dict['order']
            self.flavor = post_dict['flavor']
            # self.tags   = post_dict['tags'] TODO
            self.tags   = [None]
            self.n_per_page = int(post_dict['n_per_page'])
        else:
            self.mode   = 'drill'     # TODO 既存のユーザ設定ファイルにメンバがないとき
            self.qn     = 3           # 'ExamConf' object has no attribute 'mode' とかになるのを
            self.order  = 'random'    # なんとかする
            self.flavor = 'ng'        # なかったら、デフォルト値でメンバを差しこむ、としたい
            self.tags   = [None]
            self.n_per_page = 2

    def __eq__(self, obj):      # TODO メンバすべてをチェック→汎化
        return (self.mode == obj.mode) and (self.qn == obj.qn) and (self.order == obj.order) and (self.flavor == obj.flavor) and (self.n_per_page == obj.n_per_page)

    def __repr__(self):         # TODO メンバすべてをプリント→汎化
        return '<ExamConf mode:%s, qn:%d, order:%s, flavor:%s, tags:%r, n_per_page:%d>' % (self.mode, self.qn, self.order, self.flavor, self.tags, self.n_per_page)

    def to_dict(self):          # TODO メンバすべてを辞書に→汎化
        return {'mode':self.mode, 'qn':self.qn, 'order':self.order, 'flavor':self.flavor, 'n_per_page':self.n_per_page}

class Result(object):
    def __init__(self, i, q, your_ans):
        self.i = i

        correct_ans = q.correct_answer()
        if set(correct_ans) == set(your_ans):
            self.typ_str = Markup('&#9711;')        # まる
            self.typ_class = 'correct'
        else:
            self.typ_str = Markup('&#10005;')       # ばつ
            self.typ_class = 'wrong'
        
        opts = []
        for qo in q.opts:
            o = qo
            o.your_ans = '+' if o.onum in your_ans else None
            opts.append(o)
            
        self.q = q
        self.q.opts = opts
                
    def is_correct(self):
        return self.typ_class == 'correct'



class ExamResult(ObjList):
    def __init__(self, qpages, ans_list):
        l = []
        for i,(q,a) in enumerate(zip(util.flatten(qpages), ans_list), 1):
            assert i == q.i == a.i
            l.append(Result(i, q, a.ans))
        self._list = l

    def get_score(self):        # TODO refactoring: History's same function
        correct_answers = filter(lambda x: x.is_correct(), self._list)
        len_all  = len(self._list)
        len_corr = len(list(correct_answers))
        score = 0 if (len_corr == 0) or (len_all == 0) else round(len_corr / len_all * 100, 1)
        
        return (len_corr, len_all, score)

    def summarize(self):
        return tuple(map(lambda x: {'typ':x.typ_class, 'ad':x.q.ad, 'qnum':x.q.qnum}, self._list))

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
