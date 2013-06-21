# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 11:12:37 2013

@author: g
"""

import gevent
import random

def task(pid):
    """
    Some non-deterministic task
    """
#    gevent.sleep(random.randint(0,2))
    gevent.sleep(2)
    print('Task', pid, 'done')

def synchronous():
    for i in range(1,10):
        task(i)

def asynchronous():
    threads = [gevent.spawn(task, i) for i in xrange(10)]
    gevent.joinall(threads)

print('Synchronous:')
synchronous()

print('Asynchronous:')
asynchronous()
