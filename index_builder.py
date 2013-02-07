#coding:utf8
import jieba
import global_define
from xml_parser import XMLParser

class IndexBuilder:
    def __init__(self):
        self.__parser = XMLParser(global_define.XML_NODE_NAME,global_define.XML_TAG_NAME_LIST)
        
        pass

    def _get_xml_files(self):
    

    def run(self):
        
        pass

if __name__ == "__main__":
    xmlparser.fromfile("guide.xml")
    tmp = xmlparser.run()
    title_list = map(lambda x:x[global_define.XML_TAG_NAME_TITLE], tmp)
    segments_list = map(lambda x:jieba.cut(x), title_list)
    for segments in segments_list:
        for segment in segments:
            print segment
        break
    
