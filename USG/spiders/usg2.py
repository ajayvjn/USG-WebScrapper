from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.item import Item, Field



class UsgItem(Item):
    url = Field()

class ExampleSpider(CrawlSpider):
    name = 'a'
    allowed_domains = ['en.wikipedia.org', 'stackoverflow.com']
    start_urls = ['http://stackoverflow.com/questions/22851985/scraping-data-from-wikipedia-using-scrapy-why-when-do-errors-occur-due-to-proc']

    def start_requests(self):

        self.headers = {'referer':'https://www.google.com/','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        for i,url in enumerate(self.start_urls):
            yield Request(url, cookies={'over18':'1'}, callback=self.parse_page1, headers=self.headers)


    def parse_page1(self, response):
        print "<<==================START==================>>"
        print response
        a = Selector(response).xpath('//tr/td[2]/div/div[3]/a/@href').extract()

        print a
        print "<<===================END===================>>"

        item = UsgItem()
        item['url'] = response.url
        for i,url in enumerate(a):
            request=Request("http://stackoverflow.com"+url, cookies={'over18':'1'}, callback=self.parse_page2, headers=self.headers)
            request.meta['item'] = item
            yield request

    def parse_page2(self, response):
        print "<<==================START2==================>>"
        print response

        a = Selector(response).xpath('//*[@id="top-tags"]/div/div[1]/div/div/div/div[1]/text()').extract()
        print a[1].strip()
        print "<<===================END2===================>>"

        with open("/home/ajay/Desktop/Output.csv", "a") as text_file:
            text_file.write(a[1].strip()+"\t")

        item = response.meta['item']
        item['url'] = response.url
        return item