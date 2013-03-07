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
        keyword = params.get(self.__get_k, [""])[0]
        res = self.search(keyword)
        res = '<br/>'.join(res)
        ret_html = '<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"></head><body>%s</body></html>' %res
        self.wfile.write(ret_html)
        
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
        title_list = list()
        for item_list in temp:
            for item in item_list:
                (filepath,line_no) = item.split("#")
                line_no = int(line_no)
                title,link = self._parse(filepath, line_no)
                title_list.append(title)
            
        return title_list

    def _parse(self, file_path, line_no):
        for i,line in enumerate(open(file_path,"r")):
            if i == line_no:
                return map(lambda x:x.strip(), line.split("\t"))
        logger.critical("file_path[%s %s] error" %(file_path, line_no))
        return ("","")

if __name__ == "__main__":
    httpd = BaseHTTPServer.HTTPServer(("", 8000), MyHTTPRequestHandler)
    httpd.serve_forever()
