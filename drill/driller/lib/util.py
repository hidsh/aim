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

def get_score(func, answers):
    corrects = filter(lambda x: x.is_correct(), answers)
    len_all  = len(answers)
    len_corr = len(list(corrects))
    score = 0 if len_corr == 0 else round(len_corr / len_all * 100, 1)
    
    return (len_corr, len_all, score)

    
##
if __name__ == '__main__':
    print('%r' % split_seq([x for x in range(20)], 3))

    for ad in range(1985, 1995):
        nengo, jy = jpn_year(ad)
        print ('%04d = %s %2d' % (ad, nengo, jy))

    print('%r' % split_seq(3, range(20)))
