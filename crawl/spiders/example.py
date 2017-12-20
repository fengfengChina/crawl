# -*- coding: utf-8 -*-
import scrapy
from crawl.items import CrawlItem
# import CrawlItem


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ["jianshu.com"]
    urls = [
        "http://www.jianshu.com/u/417f8d8de4ba"
    ]

    def start_requests(self):
        header = {
            "GET": "http://www.jianshu.com/u/417f8d8de4ba HTTP/1.1",
            "Host": "www.jianshu.com",
            "Proxy-Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/\
            537.36", "Accept": "text/html,application/xhtml+xml,application/xm\
            l;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }
        for url in self.urls:
            yield scrapy.Request(url=url, headers=header, callback=self.parse)

    def parse(self, response):
        self.log('===========')
        for sel in response.css("ul.note-list li"):
            jianshu = CrawlItem()
            jianshu['name'] = sel.css('a.title::text').extract_first()

            self.log(sel.css('a.title::text').extract_first())
            self.log('info ===> %s' % sel.css(
                'p.abstract::text').extract_first())
            jianshu['info'] = sel.css('p.abstract::text').extract_first()
            jianshu['link'] = sel.css('a.title::attr(href)').extract_first()
            self.log('link ===> %s' % sel.css(
                'a.title::attr(href)').extract_first())
            yield jianshu

        # page = response.url.split("/")[-1]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
