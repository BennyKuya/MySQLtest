# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 23:42:36 2020

@author: Administrator
"""

import datetime
import requests
from lxml import etree

import time
import pymysql

import re
from user_agent import agent


class ShanXiSpider(object):
    def __init__(self):
        self.connect = pymysql.connect(host='139.129.246.77',user='ceshi',password='ceshi@123',db='hegang2',charset='utf8')
        self.cursor = self.connect.cursor() 
    def date_time(self):
        str_now = datetime.datetime.now().strftime('%b-%d-%Y %H:%M:%S')
        now_time = datetime.datetime.strptime(str_now, '%b-%d-%Y %H:%M:%S')
        return now_time
    def GetHtml(self,url):
        headers = {'User-Agent':agent()}
        response = requests.get(url,headers=headers)
        response.encoding = 'utf8'
        return response.text 
    def SpiderMain(self,typename,typecode):
        pageNo = 1
        while True:
        
            url = 'http://www.ccgp-shanxi.gov.cn/view.php?app=&type=&nav={}&page={}'.format(typecode,pageNo)
            html = self.GetHtml(url)
            source = etree.HTML(html)
            links = source.xpath('.//table[@id="node_list"]/tbody/tr/td[1]/a/@href')
            links = ['http://www.ccgp-shanxi.gov.cn/'+item for item in links]
            titles = source.xpath('.//table[@id="node_list"]/tbody/tr/td/a/@title')
            
            areas = source.xpath('.//table[@id="node_list"]/tbody/tr/td[2]/text()')
            publictimestrs = source.xpath('.//table[@id="node_list"]/tbody/tr/td[4]/text()')
            publictimes = [datetime.datetime.strptime(timetoken[1:-1],'%Y-%m-%d') for timetoken in publictimestrs]
            exp_flag = False
            for link,title,area,publictime in zip(links,titles,areas,publictimes):
                try:
                    websource = self.GetHtml(link)
                    content = websource.replace('\'','')
                    
                    typelists = ['招标公告','磋商公告','谈判公告','询价公告','废标公告','中标公告','成交公告','中标结果公告','更正公告','延期公告','变更公告']
                    if typename == '招标公告':               
                        tenderingtype = '招标公告'
                    elif typename == '结果公告':
                        tenderingtype = '结果公告'
                    else:
                        tenderingtype = '变更公告'
                            
                    for tentype in typelists:
                        if tentype in title:
                            tenderingtype = tentype
                            break
                        else:
                            continue
    #                project_contact = ''.join(re.findall(re.compile('项目联系人：(.*?)</p>',re.S),websource))
    #                project_tel = ''.join(re.findall(re.compile('电话：(.*?)</p>',re.S),websource))
                    
                    first_announcement_timestr = ''.join(re.findall(re.compile('首次公告日期：(.*?)</p>',re.S),websource))
                    first_announcement_timestr = '-'.join(re.findall(re.compile('(\d+)',re.S),first_announcement_timestr))
                    if first_announcement_timestr != '':
                        first_announcement_time = datetime.datetime.strptime(first_announcement_timestr,'%Y-%m-%d')
                    else:
                        first_announcement_time = ''
                    
                    if first_announcement_time == '':
                        sql = "insert into zhaobiao_tb(`tenderingtype`,`area`,`url`,`title`,`content`,`announcement_time`,`collect_time`,`collectid`,`collect_source`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(tenderingtype,area,link,title,content,publictime,self.date_time(),55,'山西政府采购网') 
                    else:
                        sql = "insert into zhaobiao_tb(`tenderingtype`,`area`,`url`,`title`,`content`,`announcement_time`,`first_announcement_time`,`collect_time`,`collectid`,`collect_source`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(tenderingtype,area,link,title,content,publictime,first_announcement_time,self.date_time(),55,'山西政府采购网') 
                    self.cursor.execute(sql)
                    self.connect.commit()
                    print('===={} {} 《{}》入库成功！！===='.format(typename,publictime,title))
                    print('\n')
                    time.sleep(2)
#                    print(first_announcement_time)
#                    time.sleep(2)
                except Exception as e:
                    if "Duplicate entry" in str(e):
                        print('============={} 数据重复入库，程序提前终止.......=========='.format(typename))
                        print('\n')
                        exp_flag = True
                        break  
            if exp_flag is True:
                break
            pageNo += 1            
            time.sleep(2)
       
    def main(self):
        while True:
            typeNames = ['招标公告','结果公告','变更公告']
            typeCodes = ['100','104','105']
            
            for typename,typecode in zip(typeNames,typeCodes):
                self.SpiderMain(typename,typecode)
                time.sleep(3)
            print('@@@@@@@@@@@@@@@@@@睡眠中,下次更新时间为{}@@@@@@@@@@@@@@@'.format((datetime.datetime.now()+datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")))
            time.sleep(24*60*60)
    
if __name__ == '__main__':
    shanxi = ShanXiSpider()
    shanxi.main()
