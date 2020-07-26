# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 18:49:33 2017

@author: Yang
"""

import requests
import json
import time
import datetime
import pymysql
from user_agent import agent
import re
import pandas as pd


class YunNanSpider(object):
    def __init__(self):
        self.connect = pymysql.connect(host='139.129.246.77',user='ceshi',password='ceshi@123',db='hegang2',charset='utf8')
        self.cursor = self.connect.cursor()
        self.tenderingtypes = ['竞争性谈判成交公告','成交公告','成交结果公告','竞争性磋商成交结果公告','中标公告','中标结果公告','单一来源采购成交结果公告','成交结果公告']

    def GetHtml(self,url):
        headers = {'User-Agent':agent()}
        response = requests.get(url,headers=headers)
        response.encoding = 'gbk'
        return response.text 
    
    def date_time(self):
        str_now = datetime.datetime.now().strftime('%b-%d-%Y %H:%M:%S')
        now_time = datetime.datetime.strptime(str_now, '%b-%d-%Y %H:%M:%S')
        return now_time
    
    def ParseWeb(self,pageNo,query_sign):
        link = 'http://www.ccgp-yunnan.gov.cn/bulletin.do?method=moreListQuery'
        headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Content-Length': '48',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': 'xincaigou=49737.2919.1072.0000; JSESSIONID=HKOKMXaOh0DsYuq6Ol76XAXIAU-29H4cTTs7plE-0d35kqf-eYus!1830886745',
                'Host': 'www.ccgp-yunnan.gov.cn',
                'Origin': 'http://www.ccgp-yunnan.gov.cn',
                'Referer': 'http://www.ccgp-yunnan.gov.cn/bulletin.do?method=moreList',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'}
        data = {        
            
            'current': pageNo,
            'rowCount': 10,
            'searchPhrase': "",
            'query_bulletintitle': "",
            'query_startTime': "",
            'query_endTime': "",
            'query_sign': query_sign
                            }
        data = requests.post(link,data=data,headers=headers)
        data.encoding = 'gbk'
        return json.loads(data.text)
        
    
    def Spidermain(self,query_sign):
        pageNo = 1
        while True:
            
            data = self.ParseWeb(pageNo,query_sign)
            Listdata = data["rows"]
            exp_flag = False
            for Jsondata in Listdata:
                try:
                    url = 'http://www.ccgp-yunnan.gov.cn/newbulletin_zz.do?method=preinsertgomodify&operator_state=1&flag=view&bulletin_id=' + Jsondata["bulletin_id"]
                    title = Jsondata["bulletintitle"]
#                    if query_sign == 2:
#                        tenderingtype = '采购结果公告'
#                        for typ in self.tenderingtypes:
#                            if typ in title:
#                                tenderingtype = typ
#                                break
#                            else:
#                                continue
#                    else:
                    tenderingtype = Jsondata["bulletinclasschina"]
                    area = Jsondata["codeName"]
                    publicTime = datetime.datetime.strptime(Jsondata["finishday"],'%Y-%m-%d')
                    
                    content = self.GetHtml(url)
                    
                    data = pd.read_html(url)
                    keyslist = data[0].iloc[:,0].tolist()
                    valueslist = data[0].iloc[:,1].tolist()
                    dict_data = {str(k).strip():str(v).strip() for k,v in zip(keyslist,valueslist)}
                    
                    purchaser_name = dict_data.get('采购单位','')
                    project_contact = dict_data.get('项目联系人','')
                    project_telstr = dict_data.get('项目联系电话','')
                    project_tel = ''.join(re.findall(re.compile('(\d+.*?\d+)'),project_telstr))
                    purchaser_address = dict_data.get('采购单位地址','')
                    purchaser_telstr = dict_data.get('采购单位联系方式','')
                    purchaser_tel = ''.join(re.findall(re.compile('(\d+.*?\d+)'),purchaser_telstr))
                    agent_name = dict_data.get('代理机构名称','')
                    agent_address = dict_data.get('代理机构地址','')
                    agent_tel = dict_data.get('代理机构联系方式','')
                    if agent_tel == '':
                        agent_telstr = ''.join(re.findall(re.compile('>代理机构联系方式</td>.*?>(.*?)</td>',re.S),content))
                        agent_tel = ''.join(re.findall(re.compile('(\d+.*?\d+)'),agent_telstr))
                    first_announcement_time = dict_data.get('首次公告日期','')
                    if first_announcement_time != '':
                        first_announcement_time = datetime.datetime.strptime(first_announcement_time,'%Y-%m-%d')
                    
                    if first_announcement_time == '':
                        sql = "insert into zhaobiao_tb(`tenderingtype`,`area`,`url`,`title`,`content`,`announcement_time`,`project_contact`,`project_tel`,`purchaser_name`,`purchaser_address`,`purchaser_tel`,`agent_name`,`agent_address`,`agent_tel`,`collect_time`,`collectid`,`collect_source`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(tenderingtype,area,url,title,content.replace('\'','').strip(),publicTime,project_contact,project_tel,purchaser_name,purchaser_address,purchaser_tel,agent_name,agent_address,agent_tel,self.date_time(),55,'云南政府采购网')
                    else:
                        sql = "insert into zhaobiao_tb(`tenderingtype`,`area`,`url`,`title`,`content`,`announcement_time`,`first_announcement_time`,`project_contact`,`project_tel`,`purchaser_name`,`purchaser_address`,`purchaser_tel`,`agent_name`,`agent_address`,`agent_tel`,`collect_time`,`collectid`,`collect_source`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(tenderingtype,area,url,title,content.replace('\'','').strip(),publicTime,first_announcement_time,project_contact,project_tel,purchaser_name,purchaser_address,purchaser_tel,agent_name,agent_address,agent_tel,self.date_time(),55,'云南政府采购网')
                    
                    self.cursor.execute(sql)
                    self.connect.commit()
                    print('===={} {} 《{}》入库成功！！===='.format(tenderingtype,publicTime,title))
                    print('\n')
                    time.sleep(2)
                except Exception as e:
                    if "Duplicate entry" in str(e):
                        print('=============数据重复入库，程序提前终止.......================')
                        print('\n')
                        exp_flag = True
                        break  
            if exp_flag is True:
                break
            pageNo += 1            
            time.sleep(2)
                
                
    def main(self):
        while True:
            typeNames = ['招标/预审/谈判/磋商/询价公告','澄清、更正、终止公告','中标、成交公告']
            query_signS = [1,7,2]

            for typeName,query_sign in zip(typeNames,query_signS):
                print('^^^^^^^^^^^^^^^^^^^{}^^^^^^^^^^^^^^^^^^^^^^'.format(typeName))
                self.Spidermain(query_sign)
                time.sleep(3)
            print('@@@@@@@@@@@@@@@@@@睡眠中,下次更新时间为{}@@@@@@@@@@@@@@@'.format((datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")))
            time.sleep(8*60*60)
            
if __name__ == '__main__':
    yunnan = YunNanSpider()
    yunnan.main()
    
    
    
    




