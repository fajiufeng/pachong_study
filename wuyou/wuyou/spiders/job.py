# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.request import urlopen

class JobSpider(scrapy.Spider):
    name = 'job'
   # allowed_domains = ['https://www.hnzzjob.com/']
    start_urls = ['https://www.hnzzjob.com/']

    def parse(self, response):     #提取打开页面中的url地址
        #print(response.text)
        findp=response.xpath('//div/li[@class="jobs"]')
        for solop in findp:
            #print("网址是 ", solop)
            url=solop.xpath('./a/@href').get()
            if url:
                completeurl='https://www.hnzzjob.com'+url
                #print("完整网址:",completeurl)
                yield scrapy.Request(completeurl,callback=self.parseDetail)

    def parseDetail(self,response):  #提取详细页面的相关字段
        print('当前查询的网址是:', response.url)
        gongsi=response.xpath('//div[@id="com_right"]/h1/text()').get(default='')
        zhiwei=response.xpath('//div[@class="jobtitle"]/div[@class="title-l"]/text()').get(default='')
        xinzi=response.xpath('//div[@id="context0"]/div[1]/div[5]/text()').get(default='')

        emailRegex = re.compile(r'[A-Za-z0-9\u4e00-\u9fa5]+(@|#)[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+')
        emailStr = emailRegex.search(response.text)
        if emailStr:
            email = emailStr.group()[0:32]
        else:
            email= '无'

        lianxiRegex=re.compile(r'\(?i\)广告|合作|商务|联系|我们|contact|邮箱|电话|line|tel') #\(?i\)
        lianxiStr = lianxiRegex.search(response.text)
        if lianxiStr:
            lianxi = lianxiStr.group()[0:22]
        else:
            lianxi= '无'
        #print('联系方式', lianxi)
        #必须是字典的形式
        items={
            "公司名称": gongsi,
            "职位": zhiwei,
            "薪资": xinzi,
            "联系": lianxi,
            "邮箱": email,
            "网址": response.url
        }
        #print(items)
        yield items
