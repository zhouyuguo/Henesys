#!/usr/bin/python
#-*- coding:utf8-*-
import global_define
import datetime
from tools import logger

from crawler import RSSCrawler
from builder import IncrementalIndexBuilder
from builder import PrimeIndexBuilder
from parser import Parser
import os

TODAY = datetime.date.today()
class Main:
    def __init__(self):
        self.__crawler = RSSCrawler()
        self.__iibuilder = IncrementalIndexBuilder()
        self.__pibuilder = PrimeIndexBuilder()

        pass

    def wrap(self, func):
        def ret_func():
            logger.info("func [%s.%s] begin ..." %(func.__module__, func.__name__))
            begin_t = datetime.datetime.now()
            func()
            end_t = datetime.datetime.now()
            logger.info("func [%s.%s] end ... " %(func.__module__, func.__name__))
            logger.info("consume time %s" %(end_t - begin_t))
        return ret_func
        pass

    def run(self):

        xml_dir  = os.path.join(global_define.XML_DIR,str(TODAY))
        #self.__crawler.run(xml_dir)

        data_dir = os.path.join(global_define.DATA_DIR, str(TODAY))
        iindex_dir = os.path.join(global_define.INDEX_INCREMENTAL_DIR, str(TODAY))
        self.__iibuilder.run(xml_dir, data_dir, iindex_dir)
        #run = self.wrap(self.__crawler.run)
        #run()
        
        #run = self.wrap(self.__iibuilder.run)
        #run()
        
        #run = self.wrap(self.__pibuilder.run)
        #run()

if __name__ == "__main__":
    main = Main()
    main.run()
