import cherrypy
import os
from tempfile import gettempdir
TMP_DIR = gettempdir()

class Root(object):
    title = 'Play with Python'

    def header(self):
        return '''
                <html>
                <head>
                    <title>%s</title>
                </head>
                <body>
                <h2>%s</h2>
            ''' % (self.title, self.title)

    def footer(self):
        return '''
                </body>
                </html>
            '''  

    def index(self, code=None):
        cherrypy.session['code'] = code
        output = ''
        if code is None:
            cherrypy.session['output'] = ''
        else:
            tmp_filename = os.path.join(TMP_DIR, 'my_file.dat')
            f = open(tmp_filename, 'w')
            f.write(code)
            f.close()
            f_in, f_out = os.popen4("python %s"%tmp_filename)
            output = "The result of"
            output += "<pre><font color='blue'>%s</font></pre>is: "%code
            output += "<pre><font color='green'>"
            for line in f_out.readlines():
                output += line
            output += "</font></pre>"
            cherrypy.session['output'] = output        
        return self.header()+'''
                Type in your Python code.
                <form action="index" method="GET">
                <textarea name="code" rows=5 cols=80></textarea><br/>
                <input type="submit" value="Run Python"/>
                </form>
                <br/>
                %s
            ''' % output + self.footer()
    index.exposed = True

if __name__ == '__main__':

    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),

        # sessions
        'tools.sessions.on': True,
        'tools.sessions.storage_type': "ram",
        # 'tools.sessions.storage_path': "/home/site/sessions"
        'tools.sessions.timeout': 60,        
    })

    cherrypy.quickstart(Root(), '/', {
        '/media': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    })

    
    cherrypy.quickstart(Root())
