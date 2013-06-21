#!/usr/bin/env python
# -*- coding: utf-8 -*-

# send mail utf-8 using gmail smtp server

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

    _user = "GMAIL_USER_NAME"
    _pass = "GMAIL_PASSWORD"

    smtp = smtplib.SMTP(server, port)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(_user, _pass)
    smtp.sendmail(from_addr, [to_addr], msg.as_string())
    smtp.close()

###
if __name__ == '__main__':
    body = u'拝啓　春うららかな候、ますますご清栄のこととお喜び申し上げます。\nさて私ども一同、この度…'

    send_email('sender@gmail.com', 'receiver@gmail.com', u'開店のごあいさつ', body)
