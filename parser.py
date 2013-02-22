import global_define
from tools import logger
import utilities as functs
from xml_parser import XMLParser
import datetime
import os

class Parser:
    def __init__(self):
        self.__parser = XMLParser(global_define.XML_NODE_NAME, global_define.XML_TAG_NAME_LIST)
        pass

    def parse(self, file_path):
        xml_dicts = None
        try:
            xml_dicts = self.__parser.parse(file_path)
        except Exception,e:
            logger.error("%s file parse failed. [%s]" %(file_path, e))
        return xml_dicts

    def dump(self, xml_dicts, file_id_str, day = global_define.TODAY):
        content_str = str() 
        for xml_dict in xml_dicts:
            title = xml_dict[global_define.XML_TAG_NAME_TITLE]
            link = xml_dict[global_define.XML_TAG_NAME_LINK]
            content_str += "%s\t%s\n" %(title.encode('utf8'),link)
        
        file_path = os.path.join(global_define.TEXT_DIR, str(day), file_id_str)
        functs.dump(content_str, file_path)

    def run(self, day = global_define.TODAY):
        _dir = os.path.join(global_define.XML_DIR, str(day))
        file_paths = functs.get_files(_dir)
        for i,file_path in enumerate(file_paths):
            xml_dicts = self.parse(file_path)
            if xml_dicts:
                self.dump(xml_dicts, str(i), day)
        pass

if __name__ == "__main__":
    p = Parser()
    p.run()
    pass
