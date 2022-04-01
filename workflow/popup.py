#!/usr/bin/python
# encoding: utf-8

import sys
import webview
from unicodedata import normalize
from urllib.parse import quote

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError
    query = normalize('NFC', sys.argv[1]).encode('utf-8')
    url = u'http://small.dic.daum.net/search.do?q=%s' % quote(query)
    webview.create_window('Daum Dictionary', url, width=400, height=700, on_top=True)
    webview.start()
    sys.exit(0)