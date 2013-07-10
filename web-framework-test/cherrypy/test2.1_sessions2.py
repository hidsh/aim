#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cherrypy
from functools import reduce    # >= python3

html_header = '<html><head></head><body>'
html_footer = '</body></html>'

fmt_index = '''
<pre style="border: 1px black dotted">%s</pre>
<form method="POST" action="receive">
<p>ユーザー名</p>
<input type="text" name="user" value="%s">
<p>発言</p>
<input type="text" name="comment" value="">
<input type="submit" value="Send"/>
</form>
'''

fmt_rec1 = '''
<p>OK.</p>
<p>your comment is stored.</p>
<p><a href="/">Back</a></p>
'''
fmt_rec2 = '''
<p>Negative.</p>
<p>Try again.</p>
<p><a href="/">Back</a></p>
'''

class SessionExample:
   def __init__(self):
      self.all_text = []
      
   @cherrypy.expose
   def index(self):
      if cherrypy.session.get('user'):
         user = cherrypy.session['user']
      else:
         user = ''
      return html_header + fmt_index % (reduce(lambda a,b: a + u'\n' + b, self.all_text, ''), user) + html_footer

   @cherrypy.expose
   def receive(self, user=None, comment=None):
      fmt = fmt_rec2

      if user:
         cherrypy.session['user'] = user

         if comment:
            self.all_text.append(user + u': ' + comment)
            fmt = fmt_rec1

      return html_header + fmt + html_footer
   
if __name__ == '__main__' :

    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,

        # sessions
        'tools.sessions.on': True,
        'tools.sessions.storage_type': "ram",
        'tools.sessions.timeout': 60,        
    })

    cherrypy.quickstart(SessionExample())

# Read more at http://www.devshed.com/c/a/Python/CherryPy-ObjectOriented-Web-Development/3/#q2q63twe4SFoSs7P.99

