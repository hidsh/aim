#! /usr/bin/env python
# -*- coding: utf-8 -*-

import markdown

head_str = '''
<head>
  <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
  <link rel="stylesheet" type="text/css" href="markdown.css" />
  <!-- mathjax beg -->
  <script type="text/x-mathjax-config">
  MathJax.Hub.Config({ tex2jax: { inlineMath: [['$','$']] }, "HTML-CSS": { scale: 140} });
  </script>
  <script type="text/javascript"
  src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML">
  </script>
  <meta http-equiv="X-UA-Compatible" CONTENT="IE=EmulateIE7" />
  <!-- mathjax end -->
</head>'''

##
if __name__ == '__main__':
    html_str = '<html>%s<body>' % head_str

    q_str = open('test_mj.md', 'r', encoding='utf-8').read()
    html_str += markdown.markdown(q_str, ['tables'])
    html_str += '</body></html>'

    open('test_mj.html', 'w', encoding='utf-8').write(html_str)
