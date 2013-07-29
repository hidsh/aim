#! /usr/bin/env python
# -*- coding: utf-8 -*-

def split_seq(seq, size):
    return [seq[i:i+size] for i in range(0, len(seq), size)]

def jpn_year(ad):
    assert ad > 1867, '昔すぎて計算できません'

    jc = [{'nengo':'平成', 'num':1988},      # 1989/ 1/ 8 -
          {'nengo':'昭和', 'num':1925},      # 1926/12/25 - 1989/ 1/ 8
          {'nengo':'大正', 'num':1911},      # 1912/ 7/30 - 1926/12/25
          {'nengo':'明治', 'num':1867}]      # 1868/ 9/ 8 - 1912/ 7/30

    for j in jc:
        x = ad - j['num']

        if x > 0:
            return (j['nengo'], x)

def flatten(l):
    from itertools import chain
    return list(chain.from_iterable(l))

def percent(part, total):
    if part  < 1: return 0
    if total < 1: return 0      # prevent 'div by 0'
    
    _pct = part / (total * 1.0) * 100

    _pct = round(_pct, 1)       # x.x
    _int = int(_pct)
    
    return _int if (_pct * 10 - _int * 10) == 0 else _pct
    
def get_score(func, answers):   # TODO
    corrects = filter(lambda x: x.is_correct(), answers)
    len_all  = len(answers)
    len_corr = len(list(corrects))
    score = 0 if len_corr == 0 else percent(len_corr / len_all * 100, 1)
    
    return (len_corr, len_all, score)



    
##
if __name__ == '__main__':
    print('%r' % split_seq([x for x in range(20)], 3))

    for ad in range(1985, 1995):
        nengo, jy = jpn_year(ad)
        print ('%04d = %s %2d' % (ad, nengo, jy))

    print('%r' % split_seq(3, range(20)))
