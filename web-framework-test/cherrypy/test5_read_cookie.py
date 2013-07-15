#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cherrypy

html_index = '''
<html><head>
  <script type="text/javascript">
    function write_cookie() {
      document.cookie = "q1=3";
      document.cookie = "q2=1";
      document.cookie = "q3=4";
    }
  </script>
</head><body>
<div><input type="button" value="クッキー書き込み" onclick="write_cookie()"></div>
<div><a href="receive">次のページへ</a></div>
</body></html>
'''

html_receive = '''
<html>
<head></head>
<body>
  <div>問1 %d</div>
  <div>問2 %d</div>
  <div>問3 %d</div>
  <div><a href="/">最初のページへ</a></div>
</body></html>
'''

class Ans:
   def __init__(self, qnum, ans):
      self.qnum = qnum
      self.ans = ans

class Example:
   @cherrypy.expose
   def index(self):
      return html_index

   @cherrypy.expose
   def receive(self):
      cookie = cherrypy.request.cookie

      answers = []
      for name in cookie.keys():
         print('%s = %s' % (name, cookie[name].value))
         answers.append(Ans(name, int(cookie[name].value)))

      from operator import attrgetter
      ll = [x.ans for x in sorted(answers, key=attrgetter('qnum'))]
      return html_receive % tuple(ll)
   
if __name__ == '__main__' :

    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
    })

    cherrypy.quickstart(Example())

