#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
    for x in range(1868, 2014):
        nengo, num = jpn_year(x)
        print '%d年: %s %2d年' % (x, nengo, num)

