#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from markdown import markdown

template = '''
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
    <link rel="stylesheet" type="text/css" href="markdown.css" />
    <!-- mathjax beg -->
    <script type="text/x-mathjax-config">
      MathJax.Hub.Config({ tex2jax: { inlineMath: [['$','$']] }, "HTML-CSS": { scale: 140} });
    </script>
    <script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML">
    </script>
    <meta http-equiv="X-UA-Compatible" CONTENT="IE=EmulateIE7" />
    <!-- mathjax end -->
  </head>
  <body>
    %s
  </body>
</html>
'''

def jpn_year(ad):
    assert ad > 1867, '昔すぎて計算できません'
    
    jc = [{'nengo':'平成', 'num':1988},      # 1989/ 1/ 8 -
          {'nengo':'昭和', 'num':1925},      # 1926/12/25 - 1989/ 1/ 8
          {'nengo':'大正', 'num':1911},      # 1912/ 7/30 - 1926/12/25
          {'nengo':'明治', 'num':1867}]      # 1868/ 9/ 8 - 1912/ 7/30
          
    for j in jc:
        x = ad - j['num']

        if x > 0:
            return (j['nengo'], x)
        
def format_opts(qnum, opts, ans):
    html = '<form method="post" action="get_answer.py"><table class="opts">\n'
    for i,line in enumerate(opts):
        cols = re.split('[ \t　]{2,}', line.strip())
        if (i == 0) and (cols == ['']): continue         # empty table head

        html += '<tr>'

        if i < 1:
            col_tag = 'th'
            inp = ''
            line_num = ''
        else:
            col_tag = 'td'
            inp = '<input type="%s" name="q%d" value="%d"/>' % ('checkbox' if type(ans) is list else 'radio',qnum, i)
            line_num = '(%d)' % i
            
        # for x in [inp, line_num] + cols:
        for x in [inp] + cols:
            html += '<%s>%s</%s>' % (col_tag, x, col_tag)
        html += '</tr>\n'
    html += '</table></form>'
    return html

def question_number_str(i, ad, qnum):
    nengo, jy = jpn_year(ad)
    return '<h2>問%d <span class="q_cap">［%d年（%s%d年） 問%d］</span></h2>' % (i, ad, nengo, jy, qnum)

def normalize_cr(md):
    return re.sub(r'(\n)+', r'\n\n', md)
    
def replace_blanks(html):
    return re.sub(r'\[(.)\]', r'<span class="blank">\1</span>', html)

    

##
if __name__ == '__main__':
    problems = json.load(open('houki_a.json', 'r', encoding='utf-8'))

    # display all
    # for x in problems:
        # print '%d - %d' % (x['YEAR'], x['NUM'])

    # 
    # for x in [x for x in problems if x['YEAR'] == 2009]:
    #     print '%d - %d' % (x['YEAR'], x['NUM'])

    out = ''
    for i, p in enumerate(problems[:3]):
        qnum = i + 1
        html_num  = question_number_str(qnum, p['YEAR'], p['NUM'])
        html_q    = replace_blanks(markdown(normalize_cr(p['Q']), ['tables']))
        html_opts = format_opts(qnum, p['OPTS'], p['A'])
        q1 ='<div class="qb">%s<div class="qbi">%s%s</div></div>' % (html_num, html_q, html_opts)
        out += template % q1

    open('exam.html', 'w', encoding='utf-8').write(out)

 
