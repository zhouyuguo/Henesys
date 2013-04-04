import global_define
from tools import logger
import utilities as functs
from xml_parser import XMLParser
import datetime
import os

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
        pass

    def parse(self, file_path):
        xml_dicts = list()
        try:
            xml_dicts = self.__parser.parse(file_path)
        except Exception,e:
            logger.error("%s file parse failed. [%s]" %(file_path, e))
        return xml_dicts

    def dump(self, xml_dicts, file_id_str, out_dir):
        content_str = str() 
        for xml_dict in xml_dicts:
            title = xml_dict[self.__XML_TAG_NAME_TITLE]
            link = xml_dict[self.__XML_TAG_NAME_LINK]
            pubDate = xml_dict[self.__XML_TAG_NAME_PUBDATE]
            desc = xml_dict[self.__XML_TAG_NAME_DESC]
            content_str += "%s\t%s\n" %(title.encode('utf8'),link)
        
        file_path = os.path.join(out_dir, file_id_str)
        functs.dump(content_str, file_path)

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
