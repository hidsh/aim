#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, date
import copy
from itertools import dropwhile

from driller.model import ObjList
from driller.lib import util
"""
class HistoryResultElement(object):
    def __init__(self, result):
        self.typ   = result.typ_class
        self.ad    = result.q.ad
        self.qnum  = result.q.qnum
        self.lv_xx = result.lv_xx
        self.lv_sign = result.lv_sign

    def __repr__(self):
        return '<HistoryResultElement %d: Q%d: %s, %s(%s)>' % (self.ad, self.qnum, self.typ, self.lv_xx, self.lv_sign)
"""
    
class History(object):
    def __init__(self, result_list, start_time, colors_old):
        self._list = result_list
        self.start_time = start_time
        self.end_time   = datetime.now()

        # for x in result_list:
            # self._list.append(HistoryResultElement(x))
        self.score  = self.get_score()
        self.colors = self._get_color_distributions(colors_old)            # colors_old is updated
        
    def _get_color_distributions(self, colors):
        for h in self._list:
            for q in colors:
                if (q['ad'] == h.q.ad) and (q['qnum'] == h.q.qnum):
                    q['lv_xx']   = h.lv_xx                                 # level is updated
                    q['lv_sign'] = h.lv_sign
                    break
        return copy.deepcopy(colors)
            
    def get_score(self):
        if [x for x in self._list if x.typ_class == 'reset']:
            return (-1, -1, 0)
        
        correct_answers = [x for x in self._list if x.typ_class == 'correct']
        len_all  = len(self._list)
        len_corr = len(correct_answers)
        percent = util.percent(len_corr, len_all)

        return (len_corr, len_all, percent)

    def get_time(self):
        total = (self.end_time - self.start_time)
        avg = total / len(self._list)
        return (util.timedelta_fmt(total), util.timedelta_fmt(avg))
    
    def find_answer(self, ad, qnum):
        for h in self._list:
            if (h.q.ad == ad) and (h.q.qnum == qnum):
                return (h.typ_class, self.start_time)
        else:
            return None


class PseudoResult(object):
    def __init__(self, q):
        self.typ_class = 'reset'
        self.q = q
        self.lv_xx = 'lv_re'
        self.lv_sign = ''                                          # dirty code


class HistoryList(ObjList):
    _MAX = 1000
    
    def __init__(self, qlist):
        self._list = []
        self.count = 0
        self.color_dists = [{'ad':q.ad, 'qnum':q.qnum, 'lv_xx':'lv_re'} for q in qlist]     # latest value (also used as initial value)

    def append(self, result_list, start_time):
        if [x for x in self._list if x.start_time == start_time]: return   # prevent overlapping

        self._list.append(History(result_list, start_time, self.color_dists))     # color_dists is updated
        self._list = self._list[-self._MAX:]                               # FIFO
        self.count += 1

    def level_reset(self, qlist):
                
        if self._list[-1].start_time == None: return                       # ignore resetting twice in a row

        rs = [PseudoResult(q) for q in qlist]
        self._list.append(History(rs, None, self.color_dists))             # reset: start_time = None
        self.count += 1
    """            
    def get_last_time(self):
        last = self._list[-1]
        total = (last.end_time - last.start_time)
        avg = total / len(last._list)
        return (util.timedelta_fmt(total), util.timedelta_fmt(avg))
    """        
    def out(self, reverse=True):
        l = [x for x in self._list if x.start_time]
        oldest = 1 if self.count < self._MAX else self.count - (self._MAX - 1)
        
        for i,x in enumerate(l, oldest):
            x.i = i
            x.date_str = x.start_time.strftime('%Y/%m/%d %H:%M')
            
        if reverse:
            l.reverse()
            
        return [] if l == [] else l

    def get_color_distribution(self, colors=None):
        if colors == None:
            colors = self.color_dists

        n     = len(colors)
        n_gr  = len([q for q in colors if q['lv_xx'] == 'lv_gr'])
        n_ye  = len([q for q in colors if q['lv_xx'] == 'lv_ye'])
        n_re  = len([q for q in colors if q['lv_xx'] == 'lv_re'])
        # TODO: adjust max value ratio
        return ((n, 100), (n_gr, util.percent(n_gr, n)), (n_ye, util.percent(n_ye, n)), (n_re, util.percent(n_re, n)))

    def get_history_chart(self):
        if self._list == []: return []

        l_gr = [0]
        l_ye = [0]
        l_re = [100]
        l_score = [0]
        l_label = ['']

        n = len(self._list)
        i = n - self._MAX + 1 if n > self._MAX else 1
        for h in self._list:
            _, gr, ye, re = self.get_color_distribution(h.colors)
            l_gr.append(gr[1])              # percent
            l_ye.append(ye[1])
            l_re.append(re[1])
            
            if h.start_time:
                l_score.append(h.score[2])
                l_label.append(h.start_time.strftime('%Y/%m/%d %H:%M') + '%5d' % i)
                i += 1
            else:                                # reset
                l_score.append(l_score[-1])      # duplicate last score
                l_label.append('Reset')
                
        return ('%r' % l_label, '%r' % l_score, '%r' % l_gr, '%r' % l_ye, '%r' % l_re)
        
    def get_ox_list(self, ad, qnum, reverse=True):
        l = tuple(filter(lambda x: x, [x.find_answer(ad, qnum) for x in self._list]))
        return tuple(reversed(l)) if reverse else l

    def get_previous(self, start_time):
        clone = copy.copy(self)
            
        l = list(dropwhile(lambda x: x.start_time != None, clone._list))
        l = l[1:] if l and l[0].start_time else clone._list
        l = [x for x in l if x.start_time == None or x.start_time < start_time]    # except newest
        clone._list = l

        return clone

    
##
if __name__ == '__main__':
    pass
