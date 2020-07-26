# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 05:32:06 2020

@author: Administrator
"""
import pymysql

import requests

import time
import re

import datetime

import random

def agent():
    user_agent_list = [
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 125LA; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)',
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]
    return random.choice(user_agent_list)
    

def areaPanBie(titleastr):
    qulist = ["和平区","河东区","河西区","南开区","河北区","红桥区","滨海新区","东丽区","西青区","津南区","北辰区","武清区","宝坻区","宁河区","静海区","蓟州区"]
    area = '区级'
    for qutoken in qulist:
        if qutoken in titleastr:
            area = qutoken
            break
        else:
            continue
    return area
        
class Tianjin_caigouSpider(object):
    def __init__(self):
        self.connect = pymysql.connect(host='139.129.246.77',user='ceshi',password='ceshi@123',db='hegang2',charset='utf8')
        self.cursor = self.connect.cursor()
        self.tenderingtypelist = ['公开招标公告','竞争性磋商公告','竞争性谈判公告']
    
    def date_time(self):
        str_now = datetime.datetime.now().strftime('%b-%d-%Y %H:%M:%S')
        now_time = datetime.datetime.strptime(str_now, '%b-%d-%Y %H:%M:%S')
        return now_time
    
    def GetHtml(self,url):
        headers = {'User-Agent':agent()}
        response = requests.get(url,headers=headers)
        response.encoding = 'utf8'
        return response.text
    
    def ParseWeb(self,idcode,areais):
        pageNo = 1
        while True:
            link = 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do'
            headers  = {'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Connection': 'keep-alive',
                        'Content-Length': '69',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Cookie': 'JSESSIONID=hQSGXaHCGLtQ3akisHWk-YpBUjZdmjqNtwA9obnhgq4pbTVwPoeF!2132241801; insert_cookie=19021653',
                        'Host': 'www.ccgp-tianjin.gov.cn',
                        'Origin': 'http://www.ccgp-tianjin.gov.cn',
                        'Referer': 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=view&view=Infor&id=1665&ver=2&st=1&stmp=1595687695359',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest'}
            datashi = {        
                
                'method': 'view',
                'page': pageNo,
                'id': idcode,
                'step': 1,
                'view': 'Infor',
                'st': 1,
                'ldateQGE': '',
                'ldateQLE': ''}
            dataqu = {'method': 'view',
                    'page': pageNo,
                    'id': idcode,
                    'step': 1,
                    'view': 'Infor',
                    'ldateQGE': '',
                    'ldateQLE': ''}
            if areais == '市级':
                data = datashi
            else:
                data = dataqu
            data = requests.post(link,data,headers=headers)
            data.encoding = 'utf8'
            source = data.text
            
            linkTitleTimes = re.findall(re.compile('<li><b>.*?id=(\d+)&ver.*?title="(.*?)".*?class="time">(.*?)<',re.S),source)
            
            for token in linkTitleTimes:
                try:
                    url = 'http://www.ccgp-tianjin.gov.cn/portal/documentView.do?method=view&id={}&ver=2'.format(token[0])
                    title = token[1]
                    publicTime = datetime.datetime.strptime(token[2],'%Y-%m-%d')
                    if areais == '市级':                    
                        area = '天津市'
                    if areais == '区级':
                        area = areaPanBie(title)
                    webhtml = self.GetHtml(url)
                    content = webhtml.replace('\'','')            
                    tenderingtype = '采购公告'
                    for tendertype in self.tenderingtypelist:
                        if tendertype in title:
                            tenderingtype = tendertype
                            break
                        else:
                            continue                
                    sql = "insert into zhaobiao_tb(`tenderingtype`,`area`,`url`,`title`,`content`,`announcement_time`,`collect_time`,`collectid`,`collect_source`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(tenderingtype,area,url,title,content,publicTime,self.date_time(),55,'天津政府采购网')
                    self.cursor.execute(sql)
                    self.connect.commit()
                    print('===={} {}《{}》入库成功！！===='.format('采购公告',publicTime,title))
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
        for idcode,areais in zip(['1665','1664'],['市级','区级']):
            self.ParseWeb(idcode,areais)
            time.sleep(2)
            
class Tianjin_gengzhengSpider(object):
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
    
    def ParseWeb(self,idcode,areais):
        pageNo = 1
        while True:
            link = 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do'
            headers  = {'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Connection': 'keep-alive',
                        'Content-Length': '69',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Cookie': 'JSESSIONID=hQSGXaHCGLtQ3akisHWk-YpBUjZdmjqNtwA9obnhgq4pbTVwPoeF!2132241801; insert_cookie=19021653',
                        'Host': 'www.ccgp-tianjin.gov.cn',
                        'Origin': 'http://www.ccgp-tianjin.gov.cn',
                        'Referer': 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=view&view=Infor&id=1665&ver=2&st=1&stmp=1595687695359',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest'}
            datashi = {        
                
                'method': 'view',
                'page': pageNo,
                'id': idcode,
                'step': 1,
                'view': 'Infor',
                'st': 1,
                'ldateQGE': '',
                'ldateQLE': '' }
            dataqu = {'method': 'view',
                    'page': pageNo,
                    'id': idcode,
                    'step': 1,
                    'view': 'Infor',
                    'ldateQGE': '',
                    'ldateQLE': ''}
            if areais == '市级':
                data = datashi
            else:
                data = dataqu
            data = requests.post(link,data,headers=headers)
            data.encoding = 'utf8'
            source = data.text
            
            linkTitleTimes = ''.join(re.findall(re.compile('<li><b>·</b>.*?id=(.*?)&ver=2.*?title="()">.*?class="time">(.*?)</span>',re.S),source))
            exp_flag = False
            for token in linkTitleTimes:
                try:
                    url = 'http://www.ccgp-tianjin.gov.cn/portal/documentView.do?method=view&id={}&ver=2'.format(token[0])
                    title = token[1]
                    publicTime = datetime.datetime.strptime(token[2],'%Y-%m-%d')
                    if areais == '市级':                    
                        area = '天津市'
                    if areais == '区级':
                        area = areaPanBie(title)
                    webhtml = self.GetHtml(url)
                    first_announcement_timestr = ''.join(re.findall(re.compile('>首次公告日期：(.*?)</div>',re.S),webhtml))
                    first_announcement_time = datetime.datetime.strptime(first_announcement_timestr,'%Y-%m-%d')
                    content = webhtml.replace('\'','')            
                    tenderingtype = '更正公告'
                                   
                    sql = "insert into zhaobiao_tb(`tenderingtype`,`area`,`url`,`title`,`content`,`announcement_time`,`first_announcement_time`,`collect_time`,`collectid`,`collect_source`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(tenderingtype,area,url,title,content,publicTime,first_announcement_time,self.date_time(),55,'天津政府采购网')
                    self.cursor.execute(sql)
                    self.connect.commit()
                    print('===={} {}《{}》入库成功！！===='.format('更正公告',publicTime,title))
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
        for idcode,areais in zip(['1663','1666'],['市级','区级']):
            self.ParseWeb(idcode,areais)
            time.sleep(2)


class Tianjin_jieguoSpider(object):
    def __init__(self):
        self.connect = pymysql.connect(host='139.129.246.77',user='ceshi',password='ceshi@123',db='hegang2',charset='utf8')
        self.cursor = self.connect.cursor()
        self.tenderingtypelist = ['成交公告','中标公告','终止公告']
        
    
    def date_time(self):
        str_now = datetime.datetime.now().strftime('%b-%d-%Y %H:%M:%S')
        now_time = datetime.datetime.strptime(str_now, '%b-%d-%Y %H:%M:%S')
        return now_time
    
    def GetHtml(self,url):
        headers = {'User-Agent':agent()}
        response = requests.get(url,headers=headers)
        response.encoding = 'utf8'
        return response.text
    
    def ParseWeb(self,idcode,areais):
        pageNo = 1
        
        while True:
            link = 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do'
            headers  = {'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Connection': 'keep-alive',
                        'Content-Length': '69',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Cookie': 'JSESSIONID=hQSGXaHCGLtQ3akisHWk-YpBUjZdmjqNtwA9obnhgq4pbTVwPoeF!2132241801; insert_cookie=19021653',
                        'Host': 'www.ccgp-tianjin.gov.cn',
                        'Origin': 'http://www.ccgp-tianjin.gov.cn',
                        'Referer': 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=view&view=Infor&id=1665&ver=2&st=1&stmp=1595687695359',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest'}
            datashi = {                        
                    'method': 'view',
                    'page': pageNo,
                    'id': idcode,
                    'step': 1,
                    'view': 'Infor',
                    'st': 1,
                    'ldateQGE': '',
                    'ldateQLE': ''}
            dataqu = {'method': 'view',
                    'page': pageNo,
                    'id': idcode,
                    'step': 1,
                    'view': 'Infor',
                    'ldateQGE': '',
                    'ldateQLE': ''}
            if areais == '市级':
                data = datashi
            else:
                data = dataqu
            data = requests.post(link,data,headers=headers)
            data.encoding = 'utf8'
            source = data.text
            
            linkTitleTimes = ''.join(re.findall(re.compile('<li><b>·</b>.*?id=(.*?)&ver=2.*?title="()">.*?class="time">(.*?)</span>',re.S),source))
            exp_flag = False
            for token in linkTitleTimes:
                try:
                    url = 'http://www.ccgp-tianjin.gov.cn/portal/documentView.do?method=view&id={}&ver=2'.format(token[0])
                    title = token[1]
                    publicTime = datetime.datetime.strptime(token[2],'%Y-%m-%d')
                    tenderingtype = '采购结果公告'
                    for tendertype in self.tenderingtypelist:
                        if tendertype in title:
                            tenderingtype = tendertype
                            break
                        else:
                            continue
                    if areais == '市级':                    
                        area = '天津市'
                    if areais == '区级':
                        area = areaPanBie(title)
                    webhtml = self.GetHtml(url)
                    
                    content = webhtml.replace('\'','')            
                                                   
                    sql = "insert into zhaobiao_tb(`tenderingtype`,`area`,`url`,`title`,`content`,`announcement_time`,`collect_time`,`collectid`,`collect_source`) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(tenderingtype,area,url,title,content,publicTime,self.date_time(),55,'天津政府采购网')
                    self.cursor.execute(sql)
                    self.connect.commit()
                    print('===={} {}《{}》入库成功！！===='.format('采购结果公告',publicTime,title))
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
        for idcode,areais in zip(['2014','2013'],['市级','区级']):
            self.ParseWeb(idcode,areais)
            time.sleep(2)           
    
if __name__ == '__main__':
    while True:
        caigou = Tianjin_caigouSpider()
        caigou.main()
        gengzheng = Tianjin_gengzhengSpider()
        gengzheng.main()
        jieguo = Tianjin_jieguoSpider()
        jieguo.main()
        print('@@@@@@@@@@@@@@@@@@睡眠中,下次更新时间为{}@@@@@@@@@@@@@@@'.format((datetime.datetime.now()+datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")))
        time.sleep(24*60*60)
    
    

        
   
    
        
        
        
        
