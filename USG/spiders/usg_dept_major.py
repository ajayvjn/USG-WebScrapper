from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.item import Item, Field
import json



class UsgItem(Item):
    url = Field()

class ExampleSpider(CrawlSpider):
    name = 'dept_major'
    allowed_domains = ['colleges.usnews.rankingsandreviews.com']
    #start_urls = ['http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?format=json']
    start_urls = ['http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?format=json',
                  'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=2&format=json',
                  'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=3&format=json',
                  'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=4&format=json',
                  'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=5&format=json',
                  'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=6&format=json',
                  'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=7&format=json',
                  'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=8&format=json',
                  'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=8&format=json',
                  'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=9&format=json',
                  'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=10&format=json',
                  'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=11&format=json',
                  'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=12&format=json'
                  ]
    headers = {'Accept':'text/html,application/xhtml+xml,application/json;q=0.9,image/webp,*/*;q=0.8',
               'referer':'https://www.google.com/',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    def start_requests(self):

        # Create a new csv file for output
        self.createFile()

        for i,url in enumerate(self.start_urls):
            yield Request(url, cookies={'over18':'1'}, callback=self.parse_page1, headers=self.headers)

    def parse_page1(self, response):
        print "<<==================START==================>>"
        jsonresponse = json.loads(response.body_as_unicode())

        for i, obj in enumerate(jsonresponse['data']['results']['data']['items']):
            dept = jsonresponse['data']['results']['data']['items'][i]['searchData']['major']['displayValue']
            univ_name = jsonresponse['data']['results']['data']['items'][i]['institution']['displayName']
            for key, value in dept.iteritems():
                for i, value2 in enumerate(value):
                    self.captureDataAndWrite(univ_name, key, value2)

        # dept = jsonresponse['data']['results']['data']['items'][0]['searchData']['major']['displayValue']
        # univ_name = jsonresponse['data']['results']['data']['items'][0]['institution']['displayName']
        # print dept
        # for key, value in dept.iteritems():
        #     for i, value2 in enumerate(value):
        #         self.captureDataAndWrite(univ_name, key, value2)
                #print univ_name,  key, value2

        print "<<===================END===================>>"

    def captureDataAndWrite(self, univ_name, dept_name, major):
        # Append data to csv file
        with open("/home/ajay/Desktop/Output2.csv", "a") as text_file:
            val = univ_name+"\t"+dept_name+"\t"+major+"\n"
            print val
            text_file.write(val)

    def createFile(self):
        with open("/home/ajay/Desktop/Output2.csv", "w") as text_file:
            val = "University Name\tDepartment Name\tMajors\n"
            text_file.write(val)