import json

from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider


class UsgItem(Item):
    url = Field()


class ExampleSpider(CrawlSpider):
    name = 'usg'
    allowed_domains = ['colleges.usnews.rankingsandreviews.com']
    # start_urls = ['http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?format=json']
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
            request = Request("http://colleges.usnews.rankingsandreviews.com/best-colleges/" + value + "-" + key,
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

        # get all the data through XPATH
        univ_name = Selector(response).xpath(
            '/html/body/div[1]/div/div/div[2]/div[3]/div/div[1]/div[2]/h1/text()').extract()
        if univ_name is not None:
            print univ_name
            print "============+++++++++++++++++++++++++++++++++++++++++++++"
            univ_name = univ_name[0].strip()
            if '--' in univ_name:
                univ_name = univ_name.split("--")[0]
            else:
                univ_name = univ_name
            print univ_name
        else:
            univ_name=""
        pri_photo = Selector(response).xpath('//*[@data-agent-id="photo-stream"]/div/div/div/div/img/@src').extract()
        if pri_photo is not None:
            pri_photo = pri_photo[0]
            print pri_photo
        else:
            pri_photo=""
        ranking = Selector(response).xpath(
            '/html/body/div[1]/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/div/strong/text()').extract()
        ranking = ranking[0].strip()[1:]
        print ranking
        tuition_fees = Selector(response).xpath('//section[2]/ul/li[1]/strong/text()').extract()
        tuition_fees = tuition_fees[0].split(" ")[0]
        print tuition_fees
        room_fees = Selector(response).xpath('//*[@data-field-id="wRoomBoard"]/div/div[2]/span/text()').extract()
        room_fees = room_fees[0].split(" ")[0]
        print room_fees
        school_type = Selector(response).xpath(
            '//*[@id="content-main"]/div[1]/div[3]/div/div/div[1]/div[2]/p[1]/text()').extract()
        school_type = school_type[0].strip()
        print school_type
        univ_info = Selector(response).xpath('//*[@id="content-main"]/div[1]/div[1]/div[3]/p[1]/text()').extract()
        univ_info = univ_info[0].strip()
        print univ_info
        yr_founded = Selector(response).xpath(
            '//*[@id="content-main"]/div[1]/div[3]/div/div/div[2]/div[2]/p[1]/text()').extract()
        yr_founded = yr_founded[0].strip()
        print yr_founded
        ratio_m = Selector(response).xpath(
            '//*[@data-field-id="gStudentGenderDistribution"]/div[2]/div[2]/div/div/div[1]/div[2]/span/text()').extract()
        ratio_m = ratio_m[0].strip()[:2]
        ratio_f = Selector(response).xpath(
            '//*[@data-field-id="gStudentGenderDistribution"]/div[2]/div[2]/div/div/div[1]/div[2]/span/text()').extract()
        ratio_f = ratio_f[0].strip()[:2]
        ratio = ratio_m + ":" + ratio_f
        print ratio

        health_ins = Selector(response).xpath('//*[@data-field-id="guiAddServIns"]/div/div[2]/span/text()').extract()
        health_ins = health_ins[0].strip()
        print health_ins
        app_deadline = Selector(response).xpath(
            '//*[@data-field-id="applicationDeadline"]/div/div[2]/span/text()').extract()
        app_deadline = app_deadline[0].strip()
        print app_deadline
        acc_rate = Selector(response).xpath(
            '//*[@data-field-id="rCAcceptRate"]/div/div[2]/span/text()').extract()
        acc_rate = acc_rate[0].strip()
        print acc_rate
        total_enrol = Selector(response).xpath(
            '//*[@data-field-id="totalAllStudents"]/div/div[2]/span/text()').extract()
        total_enrol = total_enrol[0].strip()
        print total_enrol
        fin_aid_app_need = Selector(response).xpath(
            '//*[@data-field-id="gFinancialAidStatistics"]/table/tbody/tr[1]/td[2]/div[1]/text()').extract()
        fin_aid_app_need = fin_aid_app_need[0].strip()
        print fin_aid_app_need
        fin_aid_recv_need = Selector(response).xpath(
            '//*[@data-field-id="gFinancialAidStatistics"]/table/tbody/tr[3]/td[2]/div[1]/text()').extract()
        fin_aid_recv_need = fin_aid_recv_need[0].strip()
        print fin_aid_recv_need
        fin_aid_need_met = Selector(response).xpath(
            '//*[@data-field-id="gFinancialAidStatistics"]/table/tbody/tr[5]/td[2]/div[1]/text()').extract()
        fin_aid_need_met = fin_aid_need_met[0].strip()
        print fin_aid_need_met
        std_fclt_ratio = Selector(response).xpath(
            '//*[@data-field-id="vStudentFacultyRatio"]/div/div[2]/span/text()').extract()
        std_fclt_ratio = std_fclt_ratio[0].strip()
        print std_fclt_ratio
        acad_cal = Selector(response).xpath(
            '//*[@id="content-main"]/div[1]/div[3]/div/div/div[4]/div[2]/p[1]/text()').extract()
        acad_cal = acad_cal[0].strip()
        print acad_cal

        # Append data to csv file
        with open("/home/ajay/Desktop/Output.csv", "a") as text_file:
            val = univ_name + "\t" + pri_photo + "\t" + ranking + "\t" + tuition_fees + "\t" + room_fees + "\t" + school_type + "\t" \
                  + univ_info + "\t" + yr_founded + "\t" + ratio + "\t" + health_ins + "\t" + app_deadline + "\t" \
                  + acc_rate + "\t" + total_enrol + "\t" + fin_aid_app_need + "\t" + fin_aid_recv_need + "\t" \
                  + fin_aid_need_met + "\t" + std_fclt_ratio + "\t" + acad_cal + "\n"
            text_file.write(val)

    # creates new csv file with table headings.
    def createFile(self):
        with open("/home/ajay/Desktop/Output.csv", "w") as text_file:
            val = "University Name\tPrimary Photo\tRanking\tTuition Fees\tHostel Fees\tSchool Type\tUniversity Info\tYear Founded" \
                  "\tRatio (M:W)\tHealth Insurance\tApplication Deadline\tAcceptance Rate\tTotal Enrollment\tFinancial Aid Applied" \
                  "\tFinancial Aid Received\tAvg Financial Aid Met\tStudent Faculty Ratio\tAcademic Calendar\n"
            text_file.write(val)
