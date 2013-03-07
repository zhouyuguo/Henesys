
import sys,os
p = os.path.abspath(".")
if p not in sys.path:
    sys.path.insert(0,p)
import global_define
from tools import logger
import utilities as functs

class IndexDict(dict):
    def __init__(self):
        dict.__init__(self)
        files = functs.get_files(global_define.INDEX_PRIME_DIR)
        for file_path in files:
            self._load(file_path)
            

    def _load(self, file_path):
        with open(file_path, 'r') as fin:
            for line in fin:
                tmp = line.split('\t')
                word = tmp[0]
                self[word] = map(lambda x:x.strip(), tmp[1:])
        pass
        
    def run(self):
        pass

    def _parse(self, (file_path, line_no)):
        for i,line in enumerate(open(file_path,"r")):
            if i == line_no - 1:
                return map(lambda x:x.strip(), line.split("\t"))
        logger.critical("get line error")
        return ("","")

indexDict = IndexDict()


if __name__ == "__main__":
    a = MyIndexDict()
    print a._parse_title(("/home/wyy/code/Henesys/text/2013-03-05/127",21))
    for key in a:
        print a[key]
        break
