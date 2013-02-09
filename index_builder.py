#coding:utf8
import jieba
import global_define
from xml_parser import XMLParser
from tools import logger
import os
import datetime
import codecs

class IndexBuilder:
    def __init__(self):
        self.__parser = XMLParser(global_define.XML_NODE_NAME, global_define.XML_TAG_NAME_LIST)
        pass

    def _get_files(self, dir_path):
        return_list = list()
        for root, dirs, files in os.walk(dir_path):
            return_list +=  map(lambda x:os.path.join(root, x), files)
        return return_list

    def _segment(self, sentence):
        return list(jieba.cut_for_search(sentence))

    def _dump(self, file_content, file_path):
        _dir = os.path.dirname(file_path)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        with codecs.open(file_path, 'wb', 'utf-8') as fout:
            fout.write(file_content)

    def _parse(self, file_path):
        xml_dicts = None
        try:
            xml_dicts = self.__parser.parse(file_path)
        except Exception,e:
            logger.error("%s file parse failed. [%s]" %(file_path, e))
        return xml_dicts

    def dump(self, xml_dicts, file_id_str):
        content_str = str() 
        for xml_dict in xml_dicts:
            title = xml_dict[global_define.XML_TAG_NAME_TITLE]
            link = xml_dict[global_define.XML_TAG_NAME_LINK]
            content_str += "%s\t%s\n" %(title, link)
        
        day_stamp = datetime.date.today()
        file_path = os.path.join(global_define.TEXT_DIR, str(day_stamp), file_id_str)
        self._dump(content_str, file_path)
        
    def run(self):
        file_paths = self._get_files(global_define.XML_DIR)
        for i,file_path in enumerate(file_paths):
            xml_dicts = self._parse(file_path)
            if xml_dicts:
                self.dump(xml_dicts, str(i))
        pass

if __name__ == "__main__":
    ib = IndexBuilder()
    ib.run()
