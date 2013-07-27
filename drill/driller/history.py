#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from driller.model import ObjList

class HistoryResultElement(object):
    def __init__(self, summarized_result):
        # summarized_result: {'typ':typ_class, 'ad':q.ad, 'qnum':q.qnum}
        self.typ  = summarized_result['typ']
        self.ad   = summarized_result['ad']
        self.qnum = summarized_result['qnum']

    def __repr__(self):
        print('<HistoryResultElement %d: Q%d: %s>' % (self.ad, self.qnum, self.typ))
    def is_correct(self):
        return self.typ == 'correct'

    
class History(object):
    def __init__(self, summary_list, start_time):
        self.start_time = start_time
        self.end_time   = datetime.now()
        self._list = []
        self.score = (0, 0, 0)
        
        for x in summary_list:
            self._list.append(HistoryResultElement(x))
        self.score = self._get_score()

    def _get_score(self):                  # TODO refactoring: ExamResult's same function
        correct_answers = filter(lambda x: x.is_correct(), self._list)
        len_all  = len(self._list)
        len_corr = len(list(correct_answers))
        score = 0 if (len_corr == 0) or (len_all == 0) else round(len_corr / len_all * 100, 1)

        return (len_corr, len_all, score)

    def find_answer(self, ad, qnum):
        for x in self._list:
            if (x.ad == ad) and (x.qnum == qnum):
                return x.typ
        else:
            return None


class HistoryList(ObjList):
    def __init__(self, _max=500):
        self._list = []
        self._max = _max

    def append(self, hist, start_time):
        if not tuple(filter(lambda x: x.start_time == start_time, self._list)):
            self._list.append(History(hist, start_time))
            self._list = self._list[-self._max:]           # FIFO

    def reversed(self):
        return None if self._list == [] else reversed(self._list)

    def get_answer_list(self, ad, qnum, reverse=True):
        l = tuple(filter(lambda x: x, [x.find_answer(ad, qnum) for x in self._list]))
        return tuple(reversed(l)) if reverse else l
        

##
if __name__ == '__main__':
    pass
