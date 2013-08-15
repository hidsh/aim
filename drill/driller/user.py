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
        path = './user/' + self.id

        _dict = {'id':self.id, 'mail_addr':self.mail_addr, 'conf':self.conf, 'history':self.history}
        
        with open(path, 'wb') as f:
            pickle.dump(_dict, f)

    def load(self):
        path = './user/' + self.id

        try:
            with open(path, 'rb') as f:
                _dict = pickle.load(f)
        except FileNotFoundError as e:
            raise('ファイルがありません: %r' % e)
        else:
            assert self.id == _dict['id']

            self.mail_addr = _dict['mail_addr']
            self.conf      = _dict['conf']
            self.history   = _dict['history']

    def update_conf(self, new_conf):
        if self.conf != new_conf:
            self.conf = new_conf
        

##
if __name__ == '__main__':
    pass
 
