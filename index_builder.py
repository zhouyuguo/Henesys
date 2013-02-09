#coding:utf8
import jieba
import global_define
import os
import datetime
from tools import logger
import utilities  as functs

class IndexBuilder:
    def __init__(self):
        pass

    def _segment(self, sentence):
        return list(jieba.cut_for_search(sentence))
        
    def run(self):
        file_paths = functs.get_files(global_define.XML_DIR)
        for i,file_path in enumerate(file_paths):
            xml_dicts = self._parse(file_path)
            if xml_dicts:
                self.dump(xml_dicts, str(i))
        pass

if __name__ == "__main__":
    ib = IndexBuilder()
    ib.run()
