#!/usr/bin/python
#-*- coding:utf8-*-
import global_define
import time
from tools import logger

from xml_parser import XMLParser
from rss_crawler import RSSCrawler
from index_builder import IndexBuilder

class Main:
    def __init__(self):
        self.__crawler = RSSCrawler()
        self.__index_builder = IndexBuilder()
        #self.__run_list = list()
        pass

    def wrap(self, func):
        def ret_func():
            logger.info("func [%s.%s] begin ..." %(func.__module__, func.__name__))
            begin_t = time.clock()
            func()
            end_t = time.clock()
            logger.info("func [%s.%s] end ... " %(func.__module__, func.__name__))
            logger.info("consume time %s" %(end_t - begin_t))
        return ret_func
        pass

    def run(self):
        run = self.wrap(self.__crawler.run)
        run()
        
        #run = self.wrap(self.__index_builder.run)
        #run()
        
        pass


if __name__ == "__main__":
    main = Main()
    main.run()
