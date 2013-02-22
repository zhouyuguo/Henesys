#coding:utf8
import jieba
import global_define
import os
import datetime
from tools import logger
import utilities  as functs

class IncrementalIndexBuilder:
    def __init__(self):
        self.__index_dict = dict()
        self.__INDEX_THRESHOLD = 1000
        self.__index_file_sum = 0 #autoincrement
        pass

    def _segment(self, sentence):
        segments_unicode = list(jieba.cut_for_search(sentence))
        return map(lambda x:x.encode("utf8"), segments_unicode)

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
    
    def dump(self, day = global_define.TODAY):
        index_lists = map(lambda x:[x] + self.__index_dict[x], self.__index_dict)
        index_str_list = map(lambda x:'\t'.join(x) + '\n', index_lists)
        content_str = ''.join(index_str_list)

        self.__index_file_sum += 1
        index_filename = str(self.__index_file_sum)
        index_filepath = os.path.join(global_define.INDEX_INCREMENTAL_DIR, str(day), index_filename)
        functs.dump(content_str, index_filepath)

        self.__index_dict = dict()
        pass
    
    def _build(self, file_path, line_no, segment_list):
        for segment in segment_list:
            self.__index_dict.setdefault(segment,list())
            self.__index_dict[segment].append("%s#%s" %(os.path.abspath(file_path), line_no))
            if len(self.__index_dict) > self.__INDEX_THRESHOLD:
                self.dump()
        pass

    def flush(self):
        self.dump()
        pass
        
    def run(self, day = global_define.TODAY):
        _dir = os.path.join(global_define.TEXT_DIR, str(day))
        file_paths = functs.get_files(_dir)
        for file_path in file_paths:
            self.build(file_path)
        self.flush()
        pass

class PrimeIndexBuilder:
    def __init__(self):
        self.__index_dict = dict()
        
        pass

    def run(self, day = global_define.TODAY):
        self.merge_from_iindex(day)
        pass

    def dump(self):
        index_lists = map(lambda x:[x] + self.__index_dict[x], self.__index_dict)
        index_str_list = map(lambda x:'\t'.join(x) + '\n', index_lists)
        content_str = ''.join(index_str_list)

        self.__index_file_sum += 1
        index_filename = str(self.__index_file_sum)
        index_filepath = os.path.join(global_define.INDEX_INCREMENTAL_DIR, str(day), index_filename)
        functs.dump(content_str, index_filepath)

        self.__index_dict = dict()
        pass


    def _merge(self, file_path):
        with open(file_path, 'r') as fin:
            for line in fin:
                tmp = line.strip().split('\t')
                if tmp and len(tmp) >= 2:
                    word = tmp[0]
                    link_list = tmp[1:]
                    self.__index_dict.setdefault(word, list())
                    self.__index_dict[word] += link_list
                else:
                    logger.critical("line[%s] error" %line)
        
    def merge_from_iindex(self, day = global_define.TODAY):
        _dir = os.path.join(global_define.INDEX_INCREMENTAL_DIR, str(day))
        file_list = functs.get_files(_dir)
        for file_path in file_list:
            self._merge(file_path)     
        pass


if __name__ == "__main__":
    ib = PrimeIndexBuilder()
    #ib = IncrementalIndexBuilder()
    ib.run()
