#!/usr/bin/python
# encoding: utf-8

import sys

import os
from workflow import Workflow3, web
import urllib
import json
import re

def get_dictionary_data(cate, query):
    url = "http://suggest.dic.daum.net/dic_all_ctsuggest"
    params = {
        "mod": "json",
        "code": "utf_in_out",
        "cate": cate,
        "enc": "utf",
        "q": query
    }
    results = web.get(url, params)
    results.raise_for_status()
    return results.json()

def main(wf):
    cate = wf.args[0]
    args = wf.args[1]

    wf.add_item(title=f'Searching Daum {cate} dict for \'{args}\'',
                autocomplete=args,
                arg=args,
                valid=True)

    def wrapper():
        return get_dictionary_data(cate, args)

    res_json = wf.cached_data(f"{cate}_{args}", wrapper, max_age=600)

    for txt in res_json['items']:
        if len(txt) > 0:
            stxt = txt.split('|')
            wf.add_item(
                title='%s  %s' % (stxt[1], stxt[2]),
                subtitle=f'Searching Daum {cate} dict for \'{stxt[1]}\'',
                autocomplete=stxt[1],
                arg=stxt[1],
                valid=True)

    wf.send_feedback()

if __name__ == u"__main__":
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
