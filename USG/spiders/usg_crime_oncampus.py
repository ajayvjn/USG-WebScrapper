import json

from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider


class UsgItem(Item):
    url = Field()


class ExampleSpider(CrawlSpider):
    name = 'crimeon'
    allowed_domains = ['colleges.usnews.rankingsandreviews.com']
    #start_urls = ['http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?format=json']
    start_urls = [
        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?format=json',
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
        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=12&format=json',
        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=13&format=json',
        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page=14&format=json'
    ]
    headers = {'Accept': 'text/html,application/xhtml+xml,application/json;q=0.9,image/webp,*/*;q=0.8',
               'referer': 'https://www.google.com/',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    univ_urls = {}

    def start_requests(self):
        # Create a new csv file for output
        self.createFile()

        for i, url in enumerate(self.start_urls):
            yield Request(url, cookies={'over18': '1'}, callback=self.parse_page1, headers=self.headers)

    def parse_page1(self, response):
        print "<<==================START==================>>"
        # convert the string response to JSON
        jsonresponse = json.loads(response.body_as_unicode())

        # get the university name and the primary key in order to form the next url
        for i, obj in enumerate(jsonresponse['data']['results']['data']['items']):
            urlName = jsonresponse['data']['results']['data']['items'][i]['institution']['urlName']
            key = jsonresponse['data']['results']['data']['items'][i]['institution']['primaryKey']
            self.univ_urls[key] = urlName

        # urlName = jsonresponse['data']['results']['data']['items'][0]['institution']['urlName']
        # key=jsonresponse['data']['results']['data']['items'][0]['institution']['primaryKey']
        # self.univ_urls[key] = urlName

        print "<<===================END===================>>"

        item = UsgItem()
        item['url'] = response.url

        # call all the urls captured above
        for key, value in self.univ_urls.iteritems():
            request = Request("http://colleges.usnews.rankingsandreviews.com/best-colleges/" + value + "-" + key+"/campus-safety",
                              cookies={'over18': '1'}, callback=self.parse_page2, headers=self.headers)
            request.meta['item'] = item
            yield request

    def parse_page2(self, response):
        print "<<==================START2==================>>"
        self.captureDataAndWrite(response)
        print "<<===================END2===================>>"

        item = response.meta['item']
        item['url'] = response.url
        return item

    def captureDataAndWrite(self, response):

        data = {}

        # get all the data through XPATH
        univ_name = Selector(response).xpath(
            '/html/body/div[1]/div/div/div[2]/div[3]/div/div[1]/div[2]/h1/text()').extract()
        if univ_name is not None:
            univ_name = univ_name[0].strip()
            if '--' in univ_name:
                univ_name = univ_name.split("--")[0]
            else:
                univ_name = univ_name
        else:
            univ_name=""
        print univ_name

        murder_manslaughter = Selector(response).xpath(
            '//*[@data-field-id="gCrimOnCampus"]/table/tbody/tr[1]/td[4]/div[1]/text()').extract()
        murder_manslaughter = murder_manslaughter[0].strip()
        print murder_manslaughter
        data["Murder/Manslaughter"] = murder_manslaughter

        neg_manslaughter = Selector(response).xpath(
            '//*[@data-field-id="gCrimOnCampus"]/table/tbody/tr[2]/td[4]/div[1]/text()').extract()
        neg_manslaughter = neg_manslaughter[0].strip()
        print neg_manslaughter
        data["Negligence Manslaughter"] =  neg_manslaughter

        rape = Selector(response).xpath(
            '//*[@data-field-id="gCrimOnCampus"]/table/tbody/tr[3]/td[4]/div[1]/text()').extract()
        rape = rape[0].strip()
        print rape
        data["Rape"] = rape

        incest = Selector(response).xpath(
            '//*[@data-field-id="gCrimOnCampus"]/table/tbody/tr[4]/td[4]/div[1]/text()').extract()
        incest = incest[0].strip()
        print incest
        data["Incest"] = incest

        statutory_rape = Selector(response).xpath(
            '//*[@data-field-id="gCrimOnCampus"]/table/tbody/tr[5]/td[4]/div[1]/text()').extract()
        statutory_rape = statutory_rape[0].strip()
        print statutory_rape
        data["Statutory Rape"] = statutory_rape

        fondling = Selector(response).xpath(
            '//*[@data-field-id="gCrimOnCampus"]/table/tbody/tr[6]/td[4]/div[1]/text()').extract()
        fondling = fondling[0].strip()
        print fondling
        data["Fondling"] = fondling

        robbery = Selector(response).xpath(
            '//*[@data-field-id="gCrimOnCampus"]/table/tbody/tr[9]/td[4]/div[1]/text()').extract()
        robbery = robbery[0].strip()
        print robbery
        data["Robbery"] = robbery

        aggravated_assault = Selector(response).xpath(
            '//*[@data-field-id="gCrimOnCampus"]/table/tbody/tr[10]/td[4]/div[1]/text()').extract()
        aggravated_assault = aggravated_assault[0].strip()
        print aggravated_assault
        data["Aggrevated Assault"] = aggravated_assault

        burglary = Selector(response).xpath(
            '//*[@data-field-id="gCrimOnCampus"]/table/tbody/tr[11]/td[4]/div[1]/text()').extract()
        burglary = burglary[0].strip()
        print burglary
        data["Burglary"] = burglary

        motor_vehicle_theft = Selector(response).xpath(
            '//*[@data-field-id="gCrimOnCampus"]/table/tbody/tr[12]/td[4]/div[1]/text()').extract()
        motor_vehicle_theft = motor_vehicle_theft[0].strip()
        print motor_vehicle_theft
        data["Motor Vehicle Theft"] = motor_vehicle_theft

        arson = Selector(response).xpath(
            '//*[@data-field-id="gCrimOnCampus"]/table/tbody/tr[13]/td[4]/div[1]/text()').extract()
        arson = arson[0].strip()
        print arson
        data["Arson"] = arson

        for key, value in data.iteritems():
            self.writeData(univ_name, key, value)


    def writeData(self, univ_name, crime_type, crime_rate):
        # Append data to csv file
        with open("/home/ajay/Desktop/Output.csv", "a") as text_file:
            val = univ_name + "\t" + crime_type + "\t" + crime_rate +"\n"
            text_file.write(val)

    # creates new csv file with table headings.
    def createFile(self):
        with open("/home/ajay/Desktop/Output.csv", "w") as text_file:
            val = "University Name\tCrime Type\tCrime Rate\n"
            text_file.write(val)
