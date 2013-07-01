#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re

opt1 = ["　　　　ア　　　　　　　イ　　　　	ウ	",
        "　特別高圧　　　　　　高電圧　　構内",
        "　高圧　　　　　　　　危険　  　区域内",
        "　高圧又は特別高圧　　高電圧　　施設内",
        "　特別高圧　　　　　　充電中　　区域内",
        "　高圧又は特別高圧　　危険　　  構内"]

head_str = '''
<head>
  <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
  <link rel="stylesheet" type="text/css" href="markdown.css" />
</head>'''

def format_opts(opts):
    ret = '<table class="opts">'
    for i,line in enumerate(opts):
        cols = re.split('\W+', line.strip())
        if (i == 0) and (cols == ['']): continue         # empty table head

        ret += '<tr>'

        if i < 1:
            col_tag = 'th'
            line_num = ''
        else:
            col_tag = 'td'
            line_num = '(%d)' % i
            
        for x in [line_num] + cols:
            ret += '<%s>%s</%s>' % (col_tag, x, col_tag)
        ret += '</tr>'
    ret += '</table>'
    return ret


##
if __name__ == '__main__':

    html_str = '<html>%s<body>' % head_str
    html_str += format_opts(opt1)
    html_str += '</body></html>'
    
    open('test_opts.html', 'w', encoding='utf-8').write(html_str)
