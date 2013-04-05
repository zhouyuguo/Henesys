#!/usr/ali/bin/python
# -*-coding:utf-8 -*-
import urllib2,re,os
import global_define
import pickle
import subprocess
import time
import datetime
from tools import logger

class RSSCrawler:
    def __init__(self):
        self.__rss_dir_list = global_define.RSS_DIR_LIST
        self.__url_prefix = "http://rss.sina.com.cn"
        self.__xml_url_re = re.compile("%s/[^\s]+\.xml" %self.__url_prefix)
        pass

    def run(self, out_dir):
        self._crawl_xml(out_dir)

    def _crawl_xml(self, out_dir):
        xml_path_list = list()
        for url in self.__rss_dir_list:
            try:
                content = urllib2.urlopen(url, timeout = 20).read()
                xml_url_list = self.__xml_url_re.findall(content)
                for url in xml_url_list:
                    file_path = self._download(url, out_dir)
                    if file_path:
                        xml_path_list.append(file_path)
            except Exception,e:
                logger.critical("errors[%s]" %e)
                exit()
            time.sleep(2)
        return xml_path_list
        
    def _download(self, url, out_dir):
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        file_name = url.replace(self.__url_prefix,"")
        file_name = file_name.replace("/","")
        file_path = os.path.join(out_dir, file_name)

        wgetcmd = "wget %s --timeout=10 --quiet -O %s" %(url,file_path)
        if not subprocess.call(wgetcmd,shell=True):
            logger.debug('wget url[%s] finished.' %url)
        else:
            logger.critical('cmd[%s] failed.' %wgetcmd)
            return None

        logger.info('download [%s] successfully' %(url))
        return os.path.abspath(file_path)

if __name__=='__main__':
    crawler=RSSCrawler()
    crawler.run()
        
    

