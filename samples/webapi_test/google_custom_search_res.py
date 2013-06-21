# -*- coding: utf-8 -*-
# Google APIs Client Library for Python
# https://developers.google.com/api-client-library/python/start/get_started

import pickle
import pprint

if __name__ == '__main__':
  res = pickle.load(open("result.dump"))
  for i,x in enumerate(res['items']):
    print u"%d: %s: %s\n%s\n" % (i, x['title'], x['link'], x['snippet'])
  # pprint.pprint(res['items'])
