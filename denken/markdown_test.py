#! /usr/bin/env python
# -*- coding: utf-8 -*-

import markdown
import re

head_str = '''
<head>
  <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
  <link rel="stylesheet" type="text/css" href="markdown.css" />
</head>'''


def replace_blanks(html):
    return re.sub(r'\[(.)\]', r'<span class="blank">\1</span>', html)

##
if __name__ == '__main__':
    html_str = '<html>%s<body>' % head_str

    q_str = open('test.md', 'r', encoding='utf-8').read()
    html_str += markdown.markdown(q_str, ['tables'])
    html_str = replace_blanks(html_str)

    html_str += '</body></html>'

    open('test2.html', 'w', encoding='utf-8').write(html_str)
