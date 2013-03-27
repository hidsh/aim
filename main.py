#!/usr/bin/env python
# -*- coding: utf-8 -*-

greeting = 'やあ!'
vocabulary = ['こんにちわ']

def bye():
    print 'またね!'

if __name__ == '__main__':
    print greeting
    while 1:
        inp = raw_input('>')

        if inp == 'bye':
            bye()
            break
        else:
            print vocabulary[0]
            print
