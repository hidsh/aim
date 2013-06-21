# random print

from os import *
import proverb
#chdir('/Users/g/test/python/web/scraping')
l = list(proverb.proverbs.items())

import random
random.shuffle(l)
d = dict(l)

print len(d)
for i in range(10):
    print '%s --- %s' % d.popitem()

print len(d)
