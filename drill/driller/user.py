#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import pickle

class User(object):
    def __init__(self, id_or_mail):
        if '@' in id_or_mail:
            self.mail_addr = id_or_mail
            self.id = id_or_mail.split('@')[0]            # TODO
        else:
            self.mail_addr = id_or_mail + '@hoge.com'     # TODO
            self.id = id_or_mail
        self.conf    = None
        self.history = None

    def save(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../user/' + self.id)
        try:
            with open(path, 'wb') as f:
                pickle.dump(self.__dict__, f)
        except IOError as e:
            print('オブジェクトを保存できませんでした: %s: %r' % (self._path, e))
            
    def load(self):
        bak = self.history.color_dists          # backup

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../user/' + self.id)
        with open(path, 'rb') as f:
            self.__dict__ = pickle.load(f)

        self.history.color_dists = self.merge_color_dists(bak)
        
    def merge_color_dists(self, bak):
        def _in_new(ad, qnum):
            for i,c in enumerate(self.history.color_dists):
                if ad == c['ad'] and qnum == c['qnum']:
                    return i
            return -1

        for i, c in enumerate(bak):
            idx = _in_new(c['ad'], c['qnum'])
            if idx < 0: continue
            bak[i] = self.history.color_dists[idx]

        return bak

            

##
if __name__ == '__main__':
    pass
 
