import urlparse
import BaseHTTPServer
import global_define
from tools import logger
import utilities as functs

class MyHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.__index_dict = self.load_index()
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        
    def do_GET(self):
        res = urlparse.urlparse(self.path)
        params = urlparse.parse_qs(res.query, True)
        res = self.search(params['s'][0])
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

    def load_index(self):
        files = functs.get_files(global_define.INDEX_PRIME_DIR)
        _index_dict = dict()
        for file_path in files:
            with open(file_path,'r') as fin:
                for line in fin:
                    tmp = line.split('\t')
                    word = tmp[0]
                    _index_dict[word] = tmp[1:]
        return _index_dict

    def search(self, word):
        temp = map(lambda x:(self.__index_dict[x] if word in x else list()), self.__index_dict)
        ret = list()
        for item in temp:
            ret += item
        return ret

if __name__ == "__main__":
    server_class = BaseHTTPServer.HTTPServer
    handler_class = MyHTTPRequestHandler
    server_address = ("", 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
