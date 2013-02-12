#!/usr/bin/env python
# -*- coding: utf-8 -*-

greeting = 'hi!'
vocabulary = ['hello']

def bye():
	print 'see you!'

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
