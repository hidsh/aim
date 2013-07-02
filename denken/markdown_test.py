#! /usr/bin/env python
# -*- coding: utf-8 -*-

import markdown
import re

head_str = '''
<head>
  <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
  <link rel="stylesheet" type="text/css" href="markdown.css" />
</head>'''



def format_opts(opts):
    html = '<table class="opts">'
    for i,line in enumerate(opts):
        cols = re.split('[ \t　]{2,}', line.strip())
        if (i == 0) and (cols == ['']): continue         # empty table head

        html += '<tr>'

        if i < 1:
            col_tag = 'th'
            line_num = ''
        else:
            col_tag = 'td'
            line_num = '(%d)' % i
            
        for x in [line_num] + cols:
            html += '<%s>%s</%s>' % (col_tag, x, col_tag)
        html += '</tr>'
    html += '</table>'
    return html

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
