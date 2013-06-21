#!/usr/bin/env python
# -*- coding: utf-8 -*-

# send mail

from os import *
chdir('/Users/g/test/python/web/scraping')

import proverb
import random

def shuffle_proverbs(pd):
    l = list(pd.items())
    random.shuffle(l)
    d = dict(l)
    return u'%s --- %s' % d.popitem()

from email.mime.text import MIMEText
from email.Header import Header
from email.Utils import formatdate
import smtplib
def send_email(from_addr, to_addr, subject, body, server='smtp.gmail.com', port=587):
    encoding='utf-8'
    msg = MIMEText(body.encode(encoding), 'plain', encoding)
    msg['Subject'] = Header(subject, encoding)
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

    smtp = smtplib.SMTP(server, port)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(to_addr,'Link/Act')
    smtp.sendmail(from_addr, [to_addr], msg.as_string())
    smtp.close()

###
import time    
pd = proverb.proverbs
    
l =list(pd.items())
random.seed()
random.shuffle(l)
pd = dict(l)
"""
while True:
    body = u'%s --- %s' % pd.popitem()
    send_email('proverbz@automata.ro', 'hideaki.sh@gmail.com', u'今日の名言', body)
    
    time.sleep(60*60)  # every 60min
"""

for i in range(10):
    print(u'%s --- %s' % pd.popitem())
    
