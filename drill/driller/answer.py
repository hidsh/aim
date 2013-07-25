#! /usr/bin/env python
# -*- coding: utf-8 -*-

from driller.model import ObjList

class Ans(object):
    def __init__(self, n, ans):
        if type(ans) is str:
            ans = [ans]

        try:
            self.i   = int(n)                # question number
            self.ans = [int(x) for x in filter(lambda x: x!='0', ans)]
        except ValueError as e:
            print('ユーザの答えに数字以外が含まれています: %r' % e)
        except Exception as e:
            print('Unknown error: %r' e)

    def __repr__(self):
        return '%s=%r' % (self.i, self.ans)
   
class AnswerList(ObjList):
    def __init__(self, ans_dict):
        l = []
        for n,a in ans_dict.items():
            try:
                n = n.split('_')[-1]
            except Exception as e:
                print('ページ番号を示すクエリストリングにアンダーバーが含まれていません: %r' % e)
 
            l.append(Ans(n, a))
 
        from operator import attrgetter
        self._list = sorted(l, key=attrgetter('i'))


##
if __name__ == '__main__':
    pass
