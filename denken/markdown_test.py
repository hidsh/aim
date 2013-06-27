#! /usr/bin/env python
# -*- coding: utf-8 -*-

import markdown

##
if __name__ == '__main__':
    html_str = '<html><header><meta content="text/html; charset=UTF-8" http-equiv="Content-Type"></header><body>'

    md_str = open('test.md', 'r', encoding='utf-8').read()
    html_str += markdown.markdown(md_str)
    html_str += '</body></html>'

    open('test2.html', 'w', encoding='utf-8').write(html_str)
