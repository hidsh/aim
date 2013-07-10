# original: 'User Sessions' at http://www.devshed.com/c/a/Python/CherryPy-ObjectOriented-Web-Development/3/
#
# mod to work on cherrypy 3.2.2
#
import cherrypy

class SessionExample:
   @cherrypy.expose
   def index ( self ):
      if cherrypy.session.has_key('color'):
         out = "<font color='%s'>%s</font>" % (cherrypy.session['color'], cherrypy.session['color'])
      else:
         out = ""
      return out + "<form method='POST' action='setColor'>\n" + \
             "Please choose a color:<br />\n" + \
             "<select name='color'>\n" + \
             "<option>Black</option>\n" + \
             "<option>Red</option>\n" + \
             "<option>Green</option>\n" + \
             "<option>Blue</option>\n" + \
             "</select><br />\n" + \
             "<input type='submit' value='Select' />\n" + \
             "</form>"

   @cherrypy.expose
   def setColor(self, color):
      cherrypy.session['color'] = color
      return "<a href='/'>Back</a>"

# cherrypy.config.update ( file = 'development.conf' )
# cherrypy.root = SessionExample()
# cherrypy.server.start()



if __name__ == '__main__' :

    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,

        # sessions
        'tools.sessions.on': True,
        'tools.sessions.storage_type': "ram",
        # 'tools.sessions.storage_path': "/home/site/sessions"
        'tools.sessions.timeout': 60,        
    })

    cherrypy.quickstart(SessionExample())

# Read more at http://www.devshed.com/c/a/Python/CherryPy-ObjectOriented-Web-Development/3/#q2q63twe4SFoSs7P.99

