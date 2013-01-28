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


    def _crawl_xml(self):
        
        for url in self.__rss_dir_list:
            try:
                content = urllib2.urlopen(url, timeout = 20).read()
                xml_url_list = self.__xml_url_re.findall(content)
                print xml_url_list
                for url in xml_url_list:
                    self._download(url)
                
                
            except Exception,e:
                logger.critical("errors[%s]" %e)
                exit()
        
        exit()
        #ip_list=set(self.__url_ip_re.findall(page))
        url_list=[]
        for ip in ip_list:
            url=os.path.join(url_origin,ip)
            page=urllib2.urlopen(url).read()
            filename_list=self.__log_name_re.findall(page)
            filename_list=sorted(list(set(filename_list)))

            for name in filename_list:
                url_abs=os.path.join(url,name)
                if url_abs not in self.__record_set:
                    url_list.append(url_abs)

        url_list = sorted(url_list,key=lambda x:self._parse_url_stamp(x))
        logger.debug('_crawl_sort_urls[%d]:' %len(url_list))
        for url in url_list:
            logger.debug('%s' %url)

        return url_list

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
            logger.debug('wget finished.' )
        else:
            logger.critical('cmd[%s] failed.' %wgetcmd)
            return None

        logger.debug('download [%s] successfully' %(url))
        

    def gen_iter(self):
        self.init()
        url_list=self._crawl_sort_url()
        for url in url_list:
            ip = self._parse_url_ip(url)
            day_stamp = self._parse_url_stamp(url)
            logger.info('url: %s ...' %url)
            file_path=self._download_unzip(ip,url)

            yield LogFileContext(url,day_stamp,ip,file_path)

            self._update_record(url)
            logger.debug('_update_record [%s]' %url)


if __name__=='__main__':
    crawler=RSSCrawler()
    crawler._crawl_xml()
    #_iter = crawler.gen_iter()
    #for item in _iter:
    #    print item
        
    

