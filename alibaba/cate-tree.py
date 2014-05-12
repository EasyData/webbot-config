#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsonpath import jsonpath
from uuid import uuid4
import codecs
import json
import os
import requests
import sys

def crawl(id, name):

    qstr = {'callback':'cb'}
    if id:
        qstr['categoryId'] = id
    else:
        if not os.path.exists('tmp'):
            os.mkdir('tmp')

    try:
        fname = './tmp/{}.json'.format(id)
        if os.path.exists(fname):
            txt = codecs.open(fname, encoding='utf-8').read()
        else:
            txt = requests.get(url, params=qstr).text
            l,r = txt.find('{'), txt.rfind('}')
            txt = txt[l:r+1]
            with codecs.open(fname, 'wb', encoding='utf-8') as f:
                f.write(txt)
        obj = json.loads(txt)
        if not obj['success']:
            os.remove(fname)
            raise Exception()
    except:
        raise

    subitems = []
    for i in jsonpath(obj, '$.data.categories.*'):
        print >>sys.stderr, sql.format(i['id'], id, i['name']).encode('utf-8')
        if i['isLeaf']:
            subitems.append(i['name'])
        elif i['id'] not in seen:
            seen.add(i['id'])
            subitems.append(crawl(i['id'], i['name']))

    return {name: subitems}

if __name__=='__main__':

    seen = set()
    sql = u"INSERT INTO tree(id, pid, name) VALUES('{}', '{}', '{}');"
    url = 'http://go.1688.com/json/GetCategoryList.jsx'
    tree = crawl(0, u'所有')
    print json.dumps(tree)

