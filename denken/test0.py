#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random


##
if __name__ == '__main__':
    problems = json.load(open('houki_a.json'))

    # # display all
    # for x in problems:
    #     print '%d - %d' % (x['YEAR'], x['NUM'])

    # # display 2009 only
    # for x in [x for x in problems if x['YEAR'] == 2009]:
    #     print '%d - %d' % (x['YEAR'], x['NUM'])

    # # display random
    # for x in random.sample(problems, 10):
    #     print '%d - %d' % (x['YEAR'], x['NUM'])
        
    # or
    random.shuffle(problems)
    for x in problems[:10]:
        print '%d - %d' % (x['YEAR'], x['NUM'])
        




