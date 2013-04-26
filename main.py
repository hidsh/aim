#!/usr/bin/env python
# -*- coding: utf-8 -*-

greeting = 'やあ!'
vocabulary = ['こんにちわ']

def answer(inp):
    if inp == 'bye':
        print 'またね!'
        return False
    else:
        print vocabulary[0]
        return True

if __name__ == '__main__':
    print greeting

    ans = True
    while ans:
        inp = raw_input('>')
        ans = answer(inp)
                
