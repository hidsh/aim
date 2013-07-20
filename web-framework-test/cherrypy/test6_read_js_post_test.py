#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cherrypy

html_index = '''
<html><head>
  <script type="text/javascript">
    function ppost(form, dest){
      form.action=dest
      form.submit();
      return false;
    }
  </script>
</head>
<body>
  <form name="q1" method="post">
    <div><input type="checkbox" name="q1" value="1" />選択肢1</div>
    <div><input type="checkbox" name="q1" value="2" />選択肢2</div>
    <div><input type="checkbox" name="q1" value="3" />選択肢3</div>
  </form>
  <div>
    <a href="#" onclick="ppost(document.q1, 'receive')">次のページへ</a>
  </div>
</body></html>
'''

html_receive = '''
<html>
<head></head>
<body>
  <div>問1 の答え：%s</div>
  <div><a href="/">最初のページへ</a></div>
</body></html>
'''

class Ans:
   def __init__(self, qnum, ans):
      self.qnum = qnum
      self.ans = ans

class Example:
   @cherrypy.expose
   def index(self, **ans):
      return html_index

   @cherrypy.expose
   def receive(self, **ans):
      print('%r' % ans)

      if 'q1' in ans:
         from functools import reduce
         s = reduce(lambda a,b:a+', '+b, ans['q1'])
      else:
         s = '回答なし'
      
      return html_receive % s
   
if __name__ == '__main__' :

    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
    })

    cherrypy.quickstart(Example())
