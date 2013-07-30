#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, date

from driller.model import ObjList
from driller.lib import util

class HistoryResultElement(object):
    def __init__(self, summarized_result):
        # summarized_result: dict {'typ':typ_class, 'ad':q.ad, 'qnum':q.qnum}
        self.typ  = summarized_result['typ']
        self.ad   = summarized_result['ad']
        self.qnum = summarized_result['qnum']

    def __repr__(self):
        print('<HistoryResultElement %d: Q%d: %s>' % (self.ad, self.qnum, self.typ))

    def is_correct(self):
        return self.typ == 'correct'

    
class History(object):
    def __init__(self, summary_list, start_time):
        self._list = []
        self.start_time = start_time
        self.end_time   = datetime.now()
        self.score = (0, 0, 0)
        
        for x in summary_list:
            self._list.append(HistoryResultElement(x))
        self.score = self._get_score()

    def _get_score(self):                  # TODO refactoring: ExamResult's same function
        correct_answers = filter(lambda x: x.is_correct(), self._list)
        len_all  = len(self._list)
        len_corr = len(list(correct_answers))
        pct = util.percent(len_corr, len_all)

        return (len_corr, len_all, pct)

    def find_answer(self, ad, qnum):
        for x in self._list:
            if (x.ad == ad) and (x.qnum == qnum):
                return (x.typ, self.start_time)
        else:
            return None


class HistoryList(ObjList):
    _MAX = 1000
    
    def __init__(self):
        self._list = []
        self.count = 0

    def append(self, hist, start_time):
        l = list(filter(lambda x: x.start_time != start_time, self._list)) # prevent overlapping
        l.append(History(hist, start_time))
        self._list = l[-self._MAX:]           # FIFO
        self.count += 1

    def level_reset(self, ql):
        l = list(filter(lambda x: x.start_time, self._list))               # delete previous reset record
        summary_list = [{'typ':'reset', 'ad':x.ad, 'qnum':x.qnum} for x in ql]
        l.append(History(summary_list, None))                              # reset: start_time = None
        self._list = l
            
        
    def out(self, reverse=True):
        l = list(filter(lambda x: x.start_time, self._list))
        oldest = 1 if self.count < self._MAX else self.count - (self._MAX - 1)
        
        for i,x in enumerate(l, oldest):
            x.i = i
            x.date_str = x.start_time.strftime('%Y/%m/%d %H:%M')
            
        if reverse:
            l.reverse()
            
        return [] if l == [] else l

    def get_answer_list(self, ad, qnum, reverse=True):
        l = tuple(filter(lambda x: x, [x.find_answer(ad, qnum) for x in self._list]))
        return tuple(reversed(l)) if reverse else l

        
##
if __name__ == '__main__':
    pass
