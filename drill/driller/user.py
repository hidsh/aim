#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import pickle

class User(object):
    def __init__(self, mail_addr):
        self.mail_addr = mail_addr
        self.conf    = None
        self.history = None

    def save(self):
        path = './user/' + self.mail_addr

        box = {'mail_addr': self.mail_addr, 'conf': self.conf, 'history': self.history}
        
        with open(path, 'wb') as f:
            pickle.dump(box, f)

    def load(self):
        path = './user/' + self.mail_addr

        try:
            with open(path, 'rb') as f:
                box = pickle.load(f)
        except FileNotFoundError as e:
            raise('ファイルがありません %r' % e)
        else:
            assert self.mail_addr == box['mail_addr']

            self.conf    = box['conf']
            self.history = box['history']
        

##
if __name__ == '__main__':
    pass
 
