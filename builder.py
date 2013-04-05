#coding:utf8
import jieba
import global_define
import os
import datetime
from tools import logger
import utilities  as functs
from parser import Parser

class IncrementalIndexBuilder:
    def __init__(self):
        self.__DATA_ROOT_DIR = global_define.DATA_DIR
        self.__index_dict = dict()
        self.__INDEX_THRESHOLD = 10000
        self.__index_file_sum = 0 #autoincrement

        self.__parser = Parser()
        self.__TITLE_K = global_define.TITLE_K
        self.__LINK_K = global_define.LINK_K
        pass

    def _segment(self, sentence):
        segments_unicode = list(jieba.cut_for_search(sentence))
        return map(lambda x:x.encode("utf8"), segments_unicode)

    def build(self, file_path, data_out_dir, index_out_dir):
        xml_dicts = self.__parser.parse(file_path)
        for xml_dict in xml_dicts:
            (file_abspath, line_i) = self.__parser.dump(xml_dict, data_out_dir)
            title = xml_dict[self.__TITLE_K]
            segment_list = self._segment(title)
            for segment in segment_list:
                self.__index_dict.setdefault(segment, list())
                relative_path = functs.get_relative_path(file_abspath, self.__DATA_ROOT_DIR)
                if None != relative_path:
                    self.__index_dict[segment].append("%s#%s" %(relative_path, line_i))
                else:
                    self.__index_dict[segment].append("%s#%s" %(file_abspath, line_i))
                    
                    
                if len(self.__index_dict) > self.__INDEX_THRESHOLD:
                    self.dump(index_out_dir)
    
    def dump(self, out_dir):
        lines = str()
        for item in self.__index_dict.items():
            _list = functs.flatten_list(item)
            _list = map(lambda x:x.encode("utf8") if isinstance(x,unicode) else x, _list)
            line = '\t'.join(_list) + '\n'
            lines += line
            
        filename = str(self.__index_file_sum)
        filepath = os.path.join(out_dir, filename)
        functs.dump(lines, filepath)

        self.__index_file_sum += 1
        self.__index_dict = dict()
        pass
    

    def flush(self, out_dir):
        self.dump(out_dir)
        pass
        
    def run(self, in_dir, data_out_dir, index_out_dir):
        file_paths = functs.get_files(in_dir)
        for file_path in file_paths:
            self.build(file_path, data_out_dir, index_out_dir)
            pass
        self.__parser.flush(data_out_dir)
        self.flush(index_out_dir)
        pass

class PrimeIndexBuilder:
    def __init__(self):
        self.__index_dict = dict()
        self.__index_file_sum = 0 
        pass

    def run(self, day):
        self.load_prime_index()
        self.merge_incremental_index(day)
        self.dump()
        pass

    def dump(self):
        index_lists = map(lambda x:[x] + self.__index_dict[x], self.__index_dict)
        index_str_list = map(lambda x:'\t'.join(x) + '\n', index_lists)
        content_str = ''.join(index_str_list)

        self.__index_file_sum += 1
        index_filename = str(self.__index_file_sum)
        index_filepath = os.path.join(global_define.INDEX_PRIME_DIR, index_filename)
        functs.dump(content_str, index_filepath)

        self.__index_dict = dict()
        pass

    def load_prime_index(self):
        file_list = functs.get_files(global_define.INDEX_PRIME_DIR)
        for file_path in file_list:
            self._merge(file_path)

    def _merge(self, file_path):
        with open(file_path, 'r') as fin:
            for line in fin:
                tmp = line.strip().split('\t')
                if tmp and len(tmp) >= 2:
                    word = tmp[0]
                    link_list = tmp[1:len(tmp)-1] + tmp[len(tmp)-1].strip()
                    self.__index_dict.setdefault(word, list())
                    for link in link_list:
                        if link not in self.__index_dict[word]:
                            self.__index_dict[word].append(link)
                else:
                    logger.critical("line[%s] error" %line)
        
    def merge_incremental_index(self, day):
        _dir = os.path.join(global_define.INDEX_INCREMENTAL_DIR, str(day))
        file_list = functs.get_files(_dir)
        for file_path in file_list:
            self._merge(file_path)     
        pass


if __name__ == "__main__":
    #ib = PrimeIndexBuilder()
    ib = IncrementalIndexBuilder()
    ib.run('./xml','./tmp2','./tmp3')
