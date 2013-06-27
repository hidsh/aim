#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random


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

##
if __name__ == '__main__':
    problems = json.load(open('houki_a.json'))

    random.shuffle(problems)

    for x in problems[:3]:
        nengo, jy = jpn_year(x['YEAR'])
        print( '-' * 40 )
        print( '%d年(%s%d年) 問%d' % (x['YEAR'], nengo, jy, x['NUM']) )
        print()
        print( x['Q'])
        print()
        for n,y in enumerate(x['OPTS']):
            print('%s %s'% (str(n) if n>0 else '',y))
        print()
        print( '答:%s' % x['A'] )
        print()

        

