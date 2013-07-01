#! /usr/bin/env python
# -*- coding: utf-8 -*-

import markdown

head_str = '''
<head>
  <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
  <link rel="stylesheet" type="text/css" href="markdown.css" />
</head>'''

##
if __name__ == '__main__':
    html_str = '<html>%s<body>' % head_str

    q_str = open('test.md', 'r', encoding='utf-8').read()
    html_str += markdown.markdown(q_str, ['tables'])

    html_str += '</body></html>'

    open('test2.html', 'w', encoding='utf-8').write(html_str)
