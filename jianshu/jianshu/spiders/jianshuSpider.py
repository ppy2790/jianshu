#coding=utf-8
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from jianshu.items import JianshuItem
import urllib


class Jianshu(CrawlSpider):
    name='jianshu'
    start_urls=['http://www.jianshu.com/top/monthly']
    url = 'http://www.jianshu.com'

    def parse(self, response):
        item = JianshuItem()
        selector = Selector(response)
        articles = selector.xpath('//ul[@class="article-list thumbnails"]/li')

        for article in articles:
            title = article.xpath('div/h4/a/text()').extract()
            url = article.xpath('div/h4/a/@href').extract()
            author = article.xpath('div/p/a/text()').extract()

            # 下载所有热门文章的缩略图, 注意有些文章没有图片
            try:
                image = article.xpath("a/img/@src").extract()
                urllib.urlretrieve(image[0], '/Users/apple/Documents/images/%s-%s.jpg' %(author[0],title[0]))
            except:
                print '--no---image--'


            listtop = article.xpath('div/div/a/text()').extract()
            likeNum = article.xpath('div/div/span/text()').extract()

            readAndComment = article.xpath('div/div[@class="list-footer"]')
            data = readAndComment[0].xpath('string(.)').extract()[0]


            item['title'] = title
            item['url'] = 'http://www.jianshu.com/'+url[0]
            item['author'] = author

            item['readNum']=listtop[0]
            # 有的文章是禁用了评论的
            try:
                item['commentNum']=listtop[1]
            except:
                item['commentNum']=''
            item['likeNum']= likeNum
            yield item

        next_link = selector.xpath('//*[@id="list-container"]/div/button/@data-url').extract()



        if len(next_link)==1 :

            next_link = self.url+ str(next_link[0])
            print "----"+next_link
            yield Request(next_link,callback=self.parse)


