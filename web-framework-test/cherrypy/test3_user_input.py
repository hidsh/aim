import cherrypy

class InputExample:
   @cherrypy.expose
   def index (self):
      return "<form method='POST' action='submit'>\n" + \
             "E-Mail: <input type='text' name='email' />\n" + \
             "<br /><input type='submit' value='Submit' />\n" + \
             "</form>"

   @cherrypy.expose
   def submit (self, email=None):
      if email:
         return "Thank you for your submission, " + email + "."
      else:
         return "You have not submitted anything!"

if __name__ == '__main__' :   
    cherrypy.quickstart(InputExample())


# Read more at http://www.devshed.com/c/a/Python/CherryPy-ObjectOriented-Web-Development/3/#rhMmujsALwjdYFUy.99 
