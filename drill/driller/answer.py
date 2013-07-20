#! /usr/bin/env python
# -*- coding: utf-8 -*-

from driller.model import ObjList

class Ans(object):
    def __init__(self, n, ans):
        assert type(ans) is list

        try:
            self.i   = int(n)                # question number
            self.ans = [int(x) for x in filter(lambda x: x!='0', ans)]
        except ValueError:
            raise ValueError('ユーザの答えに数字以外が含まれています')
        except:
            raise

    def __repr__(self):
        return '%s=%r' % (self.i, self.ans)
   
class AnswerList(ObjList):
    def __init__(self, ans_dict):
        l = []
        for n,a in ans_dict.items():
            if type(a) is str:
                a = [a]
            assert ('_' in n)
            n = n.split('_')[-1]
 
            l.append(Ans(n, a))
 
        from operator import attrgetter
        self._list = sorted(l, key=attrgetter('i'))


##
if __name__ == '__main__':
    pass
