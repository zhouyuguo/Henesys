#!/usr/bin/python
#coding:utf8

import sys,os
p = os.path.abspath(".")
if p not in sys.path:
    sys.path.insert(0,p)
import urlparse
import BaseHTTPServer
import global_define
from tools import logger
import utilities as functs
import index

class MyHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.__get_k = "s"
        #self.__index_dict = Index
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        
    def do_GET(self):
        res = urlparse.urlparse(self.path)
        params = urlparse.parse_qs(res.query, True)
        res = self.search(params[self.__get_k][0])
        self.wfile.write(res)
        pass

    def do_POST(self):
        pass

    def run(self):
        i = raw_input()
        for key in _dict:
            if i in key:
                print key,_dict[key]
        pass


    def search(self, word):
        temp = map(lambda x:(index.indexDict[x] if word in x else list()), index.indexDict)
        ret = list()
        for item in temp:
            ret += item
        return ret


if __name__ == "__main__":
    httpd = BaseHTTPServer.HTTPServer(("", 8000), MyHTTPRequestHandler)
    httpd.serve_forever()
