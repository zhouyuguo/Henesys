from xml.etree import ElementTree

from tools import logger

class XMLParser:
    def __init__(self, node_name, tag_name_list):
        self.root = None
        self.node_name = node_name
        self.tag_name_list = tag_name_list
        pass
    
    def run(self):
        if self.root:
            node_list = self.root.getiterator(self.node_name)
            return map(lambda x:self.parse(x), node_list)
        else:
            logger.critical("self.root is none")
            return None
        
    def parse(self, node):
        #print_node(node)
        return_dict = dict()
        for tag_name in self.tag_name_list:
            tmp = node.find(tag_name)
            if tmp is not None:
                return_dict[tag_name] = tmp.text.strip()
            else:
                return_dict[tag_name] = None
        return return_dict

    def fromstring(self, xml_str):
        self.root = ElementTree.fromstring(xml_str)
        pass
    
    def fromfile(self, file_path):
        self.root = ElementTree.parse(file_path)
        pass


if __name__ == "__main__":
    xmlparser = XMLParser("item",["title","link","pubDate","description"])
    xmlparser.fromfile("guide.xml")
    tmp = xmlparser.run()
    for item in tmp:
        print item["title"]
    
    #read_xml(open('guide.xml','r').read())
