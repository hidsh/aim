# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 08:48:23 2013

@author: g
"""

import time
import gevent
from gevent import select

start = time.time()
tic = lambda: 'at %1.1f seconds' % (time.time() - start)

def gr1():
    print ('Started Polling:', tic())
    select.select([],[],[],2)
    print ('Ended Polling:', tic())

def gr2():
    print ('Started Polling:', tic())
    select.select([],[],[],2)
    print ('Ended Polling:', tic())
    
def gr3():
    print ('Hey lets do some stuff while the greenlets poll, at', tic())
    gevent.sleep()

gevent.joinall([
    gevent.spawn(gr1),
    gevent.spawn(gr2),
    gevent.spawn(gr3),
])
