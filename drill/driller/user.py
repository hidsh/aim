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
        self._path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../user/' + self.id)

    def save(self):
        try:
            with open(self._path, 'wb') as f:
                pickle.dump(self.__dict__, f)
        except IOError as e:
            print('オブジェクトを保存できませんでした: %s: %r' % (self._path, e))
            
    def load(self):
        with open(self._path, 'rb') as f:
            self.__dict__ = pickle.load(f)

    def update_conf(self, new_conf):
        if self.conf != new_conf:
            self.conf = new_conf
        

##
if __name__ == '__main__':
    pass
 
