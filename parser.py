import global_define
from tools import logger
import utilities as functs
from xml_parser import XMLParser
import datetime
import os
import re

class Parser:
    def __init__(self):
        self.__XML_NODE_NAME = global_define.XML_NODE_NAME
        self.__XML_TAG_NAME_TITLE = global_define.TITLE_K
        self.__XML_TAG_NAME_LINK = global_define.LINK_K
        self.__XML_TAG_NAME_PUBDATE = global_define.PUBDATE_K
        self.__XML_TAG_NAME_DESC = global_define.DESC_K
        self.__XML_TAG_NAME_LIST = [
            self.__XML_TAG_NAME_TITLE,
            self.__XML_TAG_NAME_LINK,
            self.__XML_TAG_NAME_PUBDATE,
            self.__XML_TAG_NAME_DESC
        ]

        self.__parser = XMLParser(self.__XML_NODE_NAME, self.__XML_TAG_NAME_LIST)

        self.__line_i = 0
        self.__file_i = 0
        self.__str = str()
        self.__THRESHOLD = 1000
        pass

    def parse(self, file_path):
        xml_dicts = list()
        try:
            xml_dicts = self.__parser.parse(file_path)
        except Exception,e:
            logger.error("%s file parse failed. [%s]" %(file_path, e))
        return xml_dicts

    def dump(self, xml_dict, out_dir):
        file_abspath = os.path.abspath(os.path.join(out_dir, str(self.__file_i)))
        line_i = self.__line_i
        xml_list = map(lambda x:xml_dict[x] if xml_dict[x] else "None", self.__XML_TAG_NAME_LIST)
        xml_list = map(lambda x:x.encode('utf8') if isinstance(x, unicode) else x, xml_list)
        xml_list = map(lambda x:re.sub("[\n\t]"," ",x), xml_list)
        self.__str += '\t'.join(xml_list) + '\n'
        self.__line_i += 1
        if self.__line_i >= self.__THRESHOLD:
            functs.dump(self.__str, file_abspath)
            self.__line_i = 0
            self.__str = str()
            self.__file_i += 1
            pass
        return (file_abspath, line_i)

    def flush(self, out_dir):
        file_path = os.path.join(out_dir, str(self.__file_i))
        functs.dump(self.__str, file_path)
        self.__line_i = 0
        self.__str = str()
        self.__file_i += 1


    def run(self, in_dir, out_dir):
        file_paths = functs.get_files(in_dir)
        for i,file_path in enumerate(file_paths):
            xml_dicts = self.parse(file_path)
            if xml_dicts:
                self.dump(xml_dicts, str(i), out_dir)
        pass

if __name__ == "__main__":
    p = Parser()
    p.run('./xml','./tmp')
    pass
