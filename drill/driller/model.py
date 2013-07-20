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

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index, value):
        self._list[index] = value

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
    def __init__(self, n, method, tags=[], n_per_page=5):
        self.n = n
        self.method = method
        self.tags = tags
        self.n_per_page = n_per_page

    def __repr__(self):
        return '<%d, %s, %r>' % (self.n, self.method, self.tags)


class Result(object):
    def __init__(self, i, q, your_ans):
        self.i = i

        correct_ans = q.correct_answer()
        print('%r / %r' % (correct_ans, your_ans))
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

    def get_score(self):
        correct_answers = filter(lambda x: x.is_correct(), self._list)
        len_all  = len(self._list)
        len_corr = len(list(correct_answers))
        
        return (len_corr, len_all, round(len_corr / len_all * 100, 1))


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
