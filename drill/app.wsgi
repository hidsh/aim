#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
# import debug

app_dir = os.path.abspath(os.path.dirname(__file__))

sys.path.append(app_dir)

import cherrypy

# global config
cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.join(app_dir, 'driller'),

        'tools.sessions.on': True,
        'tools.sessions.timeout': 60,        # 60: 60 min
        'tools.sessions.storage_type': 'file',
        'tools.sessions.storage_path': os.path.join(app_dir, 'sessions')
})

app_conf = {
    '/media': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static'
    }
}

from driller.controller import Root

application = cherrypy.Application(Root(), script_name=None, config=app_conf)
