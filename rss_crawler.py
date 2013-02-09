#!/usr/ali/bin/python
# -*-coding:utf-8 -*-
import urllib2,re,os
import global_define
import pickle
import subprocess
import time
import datetime
from tools import logger
#from tools import cleaner
#from structs import LogFileContext

class RSSCrawler:
    def __init__(self):
        self.__rss_dir_list = global_define.RSS_DIR_LIST
        self.__url_prefix = "http://rss.sina.com.cn"
        self.__xml_url_re = re.compile("%s/[^\s]+\.xml" %self.__url_prefix)
        pass

    def run(self):
        self._crawl_xml()

    def _crawl_xml(self):
        xml_path_list = list()
        for url in self.__rss_dir_list:
            try:
                content = urllib2.urlopen(url, timeout = 20).read()
                xml_url_list = self.__xml_url_re.findall(content)
                for url in xml_url_list:
                    file_path = self._download(url)
                    if file_path:
                        xml_path_list.append(file_path)
            except Exception,e:
                logger.critical("errors[%s]" %e)
                exit()
        return xml_path_list
        
    def _download(self, url):
        download_dir = global_define.XML_DIR
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)

        day_stamp = datetime.date.today()
        download_dir = os.path.abspath(os.path.join(download_dir, str(day_stamp)))
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)

        #(head,fname)=os.path.split(url)
        #file_path=os.path.join(file_dir,fname)
        file_name = url.replace(self.__url_prefix,"")
        file_name = file_name.replace("/","")
        file_path = os.path.join(download_dir, file_name)

        wgetcmd = "wget %s --quiet -O %s" %(url,file_path)
        if not subprocess.call(wgetcmd,shell=True):
            logger.debug('wget url[%s] finished.' %url)
        else:
            logger.critical('cmd[%s] failed.' %wgetcmd)
            return None

        logger.debug('download [%s] successfully' %(url))
        return os.path.abspath(file_path)
        


if __name__=='__main__':
    crawler=RSSCrawler()
    crawler.run()
        
    

