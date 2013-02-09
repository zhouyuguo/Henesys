#coding:utf8
import jieba
import global_define
import os
import datetime
from tools import logger
import utilities  as functs

class IndexBuilder:
    def __init__(self):
        self.__index_dict = dict()
        self.__INDEX_THRESHOLD = 1000
        self.__index_file_sum = 0 #autoincrement
        pass

    def _segment(self, sentence):
        return list(jieba.cut_for_search(sentence))

    def build(self, file_path):
        with open(file_path) as fin:
            for line_no, line in enumerate(fin):
                tmp_list = line.split('\t')
                if not tmp_list or len(tmp_list) != 2:
                    logger.error("split line[%s] error" %line)
                    continue
                title = tmp_list[0].strip()
                link = tmp_list[1].strip()
                segment_list = self._segment(title)
                if segment_list :
                    self._build(file_path, line_no, segment_list)
    
    def dump(self, day_stamp = datetime.date.today()):
        #index_list = sorted(self.__index_dict.items(), key=lambda x:x[0])
        index_lists = map(lambda x:[x] + self.__index_dict[x], self.__index_dict)
        index_str_list = map(lambda x:'\t'.join(x) + '\n', index_lists)
        content_str = ''.join(index_str_list)

        self.__index_file_sum += 1
        index_filename = str(self.__index_file_sum)
        index_filepath = os.path.join(global_define.INDEX_DIR, str(day_stamp), index_filename)
        functs.dump_utf8(content_str, index_filepath)
    
    def _build(self, file_path, line_no, segment_list):
        for segment in segment_list:
            self.__index_dict.setdefault(segment,list())
            self.__index_dict[segment].append("%s#%s" %(file_path, line_no))
            if len(self.__index_dict) > self.__INDEX_THRESHOLD:
                self.dump()
                self.__index_dict = dict()
        
    def run(self, day_stamp = datetime.date.today()):
        _dir = os.path.join(global_define.TEXT_DIR, str(day_stamp))
        file_paths = functs.get_files(_dir)
        for file_path in file_paths:
            self.build(file_path)
            #xml_dicts = self._parse(file_path)
        pass

if __name__ == "__main__":
    ib = IndexBuilder()
    ib.run()
