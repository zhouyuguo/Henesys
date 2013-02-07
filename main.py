#!/usr/bin/python
#-*- coding:utf8-*-
import global_define

from xml_parser import XMLParser
from rss_crawler import RSSCrawler

class Main:
    def __init__(self):
        self.__crawler = RSSCrawler()
        pass

    def run(self):
        self.__crawler._crawl_xml()

        pass


if __name__ == "__main__":
    main = Main()
    main.run()
