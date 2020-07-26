# -*- coding: utf-8 -*-
"""
Created on Mon May 11 07:04:33 2020

@author: Administrator
"""
import pymysql
import requests
import time
import re
import datetime
from user_agent import agent


class GuangDongSpider(object):
    def __init__(self):
        self.connect = pymysql.connect(host='139.129.246.77',user='ceshi',password='ceshi@123',db='hegang2',charset='utf8')
        self.cursor = self.connect.cursor()
        self.tenderingtypes_cai = ['公开招标','招标','竞争性磋商','竞争性谈判','单一来源']
        self.tenderingtypes_geng = ['更正公告']
        self.tenderingtypes_zhong = ['中标结果公告','中标（成交）公告','中标（成交）结果公告','结果公告','废标公告','成交公告','结果（废标）公告']
        
    def GetHtml(self,url):
        headers = {'User-Agent':agent()}
        response = requests.get(url,headers=headers)
        response.encoding = 'utf8'
        return response.text 
    
    def date_time(self):
        str_now = datetime.datetime.now().strftime('%b-%d-%Y %H:%M:%S')
        now_time = datetime.datetime.strptime(str_now, '%b-%d-%Y %H:%M:%S')
        return now_time
    

    def Spider(self,typecode,typename):
        pageNo = 1
        while True:
            posturl = 'http://www.ccgp-guangdong.gov.cn/queryMoreInfoList.do'
            
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                       'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       'Cache-Control': 'max-age=0',
                       'Connection': 'keep-alive',
                       'Content-Length': '245',
                       'Content-Type': 'application/x-www-form-urlencoded',
                       'Cookie': 'PortalCookie=Vj6DZm8i_4XFxWnJk3mj0ugrVDoHyVdNMbGyyytCblHEzJDECVke!1310434424; JSESSIONID=8148F52178D2608DF04C143DFF9B6314',
                       'Host': 'www.ccgp-guangdong.gov.cn',
                       'Origin': 'http://www.ccgp-guangdong.gov.cn',
                       'Referer': 'http://www.ccgp-guangdong.gov.cn/queryMoreInfoList.do',
                       'Upgrade-Insecure-Requests': '1',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
            nowtimestr = str(self.date_time()).split(' ')[0]
            data = {
                    'channelCode': typecode,
                    'issueOrgan': '',
                    'operateDateFrom': '2020-06-25',
                    'operateDateTo': nowtimestr,
                    'performOrgName': '',
                    'poor': '',
                    'purchaserOrgName':'', 
                    'regionIds': '',
                    'sitewebId': '-1',
                    'sitewebName': '',
                    'stockIndexName': '',
                    'stockNum': '',
                    'stockTypes': '',
                    'title': '',
                    'pageIndex': pageNo,
                    'pageSize': 15,
                    'pointPageIndexId': 1}
            
            response = requests.post(posturl,data=data,headers=headers)
            response.encoding = 'utf8'
            pageSource = response.text
            if 'title="' not in pageSource:
                print('没有源码，跳过。。。')
                break
            areaHref = re.findall(re.compile('onclick="selectRegion.*?>(.*?)</a>.*?href="(.*?)"',re.S),pageSource)
            areaHreflist = [[token[0],'http://www.ccgp-guangdong.gov.cn'+token[1]] for token in areaHref]
            exp_flag = False
            for item in areaHreflist:
                try:
                    area = item[0]
                    url = item[1]
                    
                    WebHTML = self.GetHtml(url)
                    
                    title = ''.join(re.findall(re.compile('<div class="zw_c_c_title">(.*?)</div>',re.S),WebHTML))
                    if typename == '采购公告':                    
                        tenderingtypeslist = self.tenderingtypes_cai
                        tenderingtypes = '采购公告'
                        for t in tenderingtypeslist:
                            if t in title:
                                tenderingtypes = t + '公告'
                                break
                            else:
                                continue                        
                            
                    elif typename == '更正公告':
                        tenderingtypeslist = self.tenderingtypes_geng
                        tenderingtypes = '更正公告'
                        for t in tenderingtypeslist:
                            if t in title:
                                tenderingtypes = t
                                break
                            else:
                                continue
                    else:
                        tenderingtypeslist = self.tenderingtypes_zhong
                        tenderingtypes = '中标公告'
                        for t in tenderingtypeslist:
                            if t in title:
                                tenderingtypes = t
                                break
                            else:
                                continue
                    collect_source = ''.join(re.findall(re.compile('<span>信息来源：(.*?)</span>',re.S),WebHTML))
                    
                    publictimestr = ''.join(re.findall(re.compile('<span>发布日期：(.*?)</span>',re.S),WebHTML))
                    publicTime = datetime.datetime.strptime(publictimestr,'%Y-%m-%d %H:%M:%S')
                    
                    purchaser_Info = ''.join(re.findall(re.compile('对本次(.*?)>发布人',re.S),WebHTML))
                    
                    purchaser_Info_name = re.findall(re.compile('名称：(.*?)</span>',re.S),purchaser_Info)
                    
                    purchaser_Info_address = re.findall(re.compile('地址：(.*?)</span>',re.S),purchaser_Info)
                    
                    purchaser_Info_tel = re.findall(re.compile('联系方式：(.*?)</span>',re.S),purchaser_Info)
                    
                    purchaser_name = purchaser_Info_name[0]
                    agent_name = purchaser_Info_name[1]
                    
                    purchaser_address = purchaser_Info_address[0]
                    agent_address = purchaser_Info_address[1]
                    
                    purchaser_tel = purchaser_Info_tel[0]
                    agent_tel  = purchaser_Info_tel[1]
                    
                    project_contact = ''.join(re.findall(re.compile('项目联系人：(.*?)</span>',re.S),purchaser_Info)).strip()
                    project_tel = ''.join(re.findall(re.compile('电话：(.*?)</span>',re.S),purchaser_Info)).strip()
                    
                    first_announcement_timestr = ''.join(re.findall(re.compile('>首次公告日期：(.*?)日',re.S),WebHTML)).strip()
                    if first_announcement_timestr != '':
                        first_announcement_timestr = '2020-' +'-'.join(re.findall(re.compile('>(\d+\d+)<',re.S),first_announcement_timestr))
                    
                        first_announcement_time = datetime.datetime.strptime(first_announcement_timestr,'%Y-%m-%d')
                    else:
                        first_announcement_time = ''
                    if first_announcement_time == '':
                        sql = "insert into zhaobiao_tb(`tenderingtype`,`area`,`url`,`title`,`content`,`announcement_time`,`project_contact`,`project_tel`,`purchaser_name`,`purchaser_address`,`purchaser_tel`,`agent_name`,`agent_address`,`agent_tel`,`collect_time`,`collectid`,`collect_source`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(tenderingtypes,area,url,title,WebHTML.replace('\'','').strip(),publicTime,project_contact,project_tel,purchaser_name,purchaser_address,purchaser_tel,agent_name,agent_address,agent_tel,self.date_time(),55,collect_source)
                    else:
                        sql = "insert into zhaobiao_tb(`tenderingtype`,`area`,`url`,`title`,`content`,`announcement_time`,`first_announcement_time`,`project_contact`,`project_tel`,`purchaser_name`,`purchaser_address`,`purchaser_tel`,`agent_name`,`agent_address`,`agent_tel`,`collect_time`,`collectid`,`collect_source`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(tenderingtypes,area,url,title,WebHTML.replace('\'','').strip(),publicTime,first_announcement_time,project_contact,project_tel,purchaser_name,purchaser_address,purchaser_tel,agent_name,agent_address,agent_tel,self.date_time(),55,collect_source)
                    
                    self.cursor.execute(sql)
                    self.connect.commit()
                    print('===={} {} 《{}》入库成功！！===='.format(tenderingtypes,publictimestr,title))
                    print('\n')
                    
                    time.sleep(4)
                except Exception as e:
                    if "Duplicate entry" in str(e):
                        print('=============数据重复入库，程序提前终止.......================')
                        print('\n')
                        exp_flag = True
                        break  
            if exp_flag is True:
                break
            pageNo += 1             
            time.sleep(5)

    def main(self):
        while True:            
            typeNames = ['采购公告','更正公告','中标公告']
            typeCodes = ['0005','0006','0008']            
            for typeName,typeCode in zip(typeNames,typeCodes):
                self.Spider(typeCode,typeName)
                time.sleep(2)
            print('@@@@@@@@@@@@@@@@@@睡眠中,下次更新时间为{}@@@@@@@@@@@@@@@'.format((datetime.datetime.now()+datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")))
            time.sleep(24*60*60)
            
            
if __name__ == '__main__':
    guangdong = GuangDongSpider()
    guangdong.main()
    
