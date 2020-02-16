# -*- coding: utf-8 -*-
import scrapy

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
        print(response.text)
        gongsi=response.xpath('//div[@id="com_right"]/h1/text()').get(default='')
        zhiwei=response.xpath('//div[@class="jobtitle"]/div[@class="title-l"]/text()').get(default='')
        xinzi=response.xpath('//div[@id="context0"]/div[1]/div[5]/text()').get(default='')
        #必须是字典的形式
        items={
            "公司名称": gongsi,
            "职位": zhiwei,
            "薪资": xinzi,
        }
        #print(items)
        yield items
