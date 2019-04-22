#coding=utf-8
import scrapy
import logging,json,re,time,random,redis
from FlightsDomestic.items import FlightsdomesticItem
from datetime import datetime,timedelta
#from scrapy_splash import SplashRequest
from scrapy_redis.spiders import RedisSpider

class CustomLogger(object):
    def __init__(self, logger_name):
        filen = datetime.now().strftime('%Y-%m-%d %H:%M')

        self.log_filen = r"/media/gumoha/资料/Scrapy/xiecheng_AirTicket/FlightsDomestic/LOG/-log-{0}.json".format(filen)
        self.log_level = logging.INFO
        self.name = logger_name  #
        self.logger = logging.getLogger(self.name)

        # 定义输出格式
        log_format = '%(asctime)s-%(name)s-%(levelname)s--%(message)s'
        self.formatter = logging.Formatter(log_format)

        # 创建一个handler，用于输出到控制台
        self.sh = logging.StreamHandler()
        self.sh.setFormatter(self.formatter)

        # 创建一个handler，用于输出到日志文件
        self.logger.setLevel(self.log_level)
        self.fh = logging.FileHandler(self.log_filen, mode='w')
        self.fh.setFormatter(self.formatter)

        self.logger.addHandler(self.sh)
        self.logger.addHandler(self.fh)

    def getlog(self):
        return self.logger



class FlightsDomesticSpider(RedisSpider):
    clog = CustomLogger('clog').getlog()
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_today = datetime.now().strftime('%Y-%m-%d')

    name = 'CtripFlights_DomesticTickets'
    allowed_domains = ['ctrip.com']

    flightsApi = 'https://flights.ctrip.com/itinerary/api/12808/products'
    flightsUrl = 'https://www.baidu.com/'

    headersApi = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate,br',
        'Connection': 'keep-alive',
        'Content-Length': '212',
        'Content-Type': 'application/json',
        'Host': 'flights.ctrip.com',
        'Origin': 'https://flights.ctrip.com',
        'TE': 'Trailers',
        'DNT': '1',
        # 'Referer': 'https://flights.ctrip.com/itinerary/oneway/ctu-syx?date=2019-03-28',
        'Referer': 'https://flights.ctrip.com',
    }

    while True:
        print('请输入需要获取的时间段(不能提前与今日:{0})\n'.format(time_today))
        pattern = re.compile(
            r'([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))')
        timeA = input('输入起始日期：')
        timeB = input('输入截止日期：')
        if pattern.search(timeA) and pattern.search(timeB):
            if (timeA >= str(time_today)) and (timeB >= str(time_today)):
                timeStart = datetime.strptime(timeA, '%Y-%m-%d')
                timeStop = datetime.strptime(timeB, '%Y-%m-%d')
                timeStep = timeStop - timeStart
                print('获取时间间隔：', timeStep)
                break
        else:
            print('输入格式错误，请重输')
            continue

    def date_range(self, start, stop):
        while start <= stop:
            yield start
            start += timedelta(days=1)

    def output_date(self, timeStart, timeStop):
        for d in self.date_range(timeStart, timeStop):
            yield (d.date())

    def connect_redis(self):
        pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password=None,
                                    encoding='utf-8', decode_responses=True)
        redisdb = redis.Redis(connection_pool=pool)
        print('链接Redis:{0} 成功'.format(redisdb))
        return redisdb

    def get_allroutedata(self):
        redisdb = self.connect_redis()
        routedata_key = 'CtripFlights_AllCitysRouteData'
        try:
            for d in redisdb.sscan_iter(routedata_key):
                d = json.loads(d)
                yield (d)
        except Exception as e:
            self.clog.error('get_allroutedata-ErrorType:{0} Error:{1}'.format(type(e), e))

    def form_postdata(self):
        try:
            for date in self.output_date(self.timeStart, self.timeStop):
                for d in self.get_allroutedata():
                    d['date'] = str(date)
                    fd = {
                        'flightWay': 'Oneway',
                        'classType': 'ALL',
                        'hasBaby': 'false',
                        'hasChild': 'false',
                        'searchIndex': '1',
                        'airportParams': [d],
                        'army': 'false',
                    }

                    yield fd
        except Exception as e:
            self.clog.error('form_postdata-ErrorType:{0} Error:{1}'.format(type(e), e))

    def start_requests(self):
        for fd in self.form_postdata():
            try:
                time.sleep(random.random() * 20)
                self.clog.info('PayloadData:{0}'.format(fd['airportParams']))
                yield scrapy.Request(url=self.flightsApi, callback=self.parse_items, method='GET',
                                     headers=self.headersApi, dont_filter=True,
                                     meta={'payloadFlag': True, 'payloadData': fd, 'payloadHeaders': self.headersApi,
                                           "datatime": self.time_now})

            except Exception as e:
                self.clog.error('Requests Type:{0}, Error:{1}'.format(type(e), e))
                self.clog.error('PayloadData:{0}'.format(fd['airportParams']))

    def parse_items(self, response):
        JSONData = json.loads(response.body_as_unicode())

        datatext = JSONData['data']

        errormsg = datatext['error']

        if errormsg is None:
            try:
                routeList = datatext['routeList']
                routeCount = len(routeList)

                for c in range(routeCount):
                    routeInfo = routeList[c]
                    legstext = routeInfo['legs']

                    legsCount = len(legstext)

                    for lc in range(legsCount):
                        legstext_dict = legstext[lc]

                        flightstext = legstext_dict['flight']

                        departureAirportInfo = flightstext['departureAirportInfo']
                        arrivalAirportInfo = flightstext['arrivalAirportInfo']

                        cabinsInfo = legstext_dict['cabins']
                        cabinsCount = len(cabinsInfo)

                        item = FlightsdomesticItem()

                        item['ErrorMsg'] = None

                        item['RouteData'] = response.meta['payloadData']['airportParams']

                        item['RouteType'] = routeInfo['routeType']
                        item['DataTime'] = response.meta['datatime']
                        item['LegType'] = legstext_dict['legType']
                        item['RouteCount'] = routeCount

                        item['FlightID'] = legstext_dict['flightId']
                        item['FlightNumber'] = flightstext['flightNumber']

                        item['FlightNumber'] = flightstext['flightNumber']
                        item['AirlineCode'] = flightstext['airlineCode']
                        item['AirlineName'] = flightstext['airlineName']

                        item['SharedFlightNumber'] = flightstext['sharedFlightNumber']
                        item['SharedFlightName'] = flightstext['sharedFlightName']

                        item['CraftTypeName'] = flightstext['craftTypeName']
                        item['CraftKind'] = flightstext['craftKind']
                        item['CraftTypeCode'] = flightstext['craftTypeCode']
                        item['CraftTypeKindDisplayName'] = flightstext['craftTypeKindDisplayName']

                        item['PunctualityRate'] = flightstext['punctualityRate']
                        item['MealType'] = flightstext['mealType']

                        departureAirportInfo_terminal = departureAirportInfo['terminal']
                        item['DepartureCityTlc'] = departureAirportInfo['cityTlc']
                        item['DepartureCityName'] = departureAirportInfo['cityName']
                        item['DepartureAirportName'] = departureAirportInfo.get('airportName')
                        item['DepartureAirportID'] = departureAirportInfo_terminal['name']
                        item['DepartureDate'] = flightstext['departureDate']

                        arrivalAirportInfo_terminal = arrivalAirportInfo['terminal']
                        item['ArrivalCityTlc'] = arrivalAirportInfo['cityTlc']
                        item['ArrivalCityName'] = arrivalAirportInfo['cityName']
                        item['ArrivalAirportName'] = arrivalAirportInfo['airportName']
                        item['ArrivalAirportID'] = arrivalAirportInfo_terminal['name']
                        item['ArrivalDate'] = flightstext['arrivalDate']

                        cabins = []
                        for i in range(cabinsCount):
                            ca = {}
                            ca['CabinID'] = cabinsInfo[i]['id']
                            ca['CabinClass'] = cabinsInfo[i]['cabinClass']
                            ca['PriceClass'] = cabinsInfo[i]['priceClass']
                            ca['SeatCount'] = cabinsInfo[i]['seatCount']
                            ca['TicketPrice'] = cabinsInfo[i]['price']['price']
                            ca['Discount'] = cabinsInfo[i]['price']['rate']
                            cabins.append(ca)

                        item['Cabins'] = cabins
                        item['CabinsCount'] = cabinsCount

                        yield item
            except Exception as e:
                self.clog.error('errormsg is None,ErrorType:{0},Error:{1}'.format(type(e),e))

        else:
            try:
                item = FlightsdomesticItem()

                msg = errormsg['message']
                routedata = response.meta['payloadData']['airportParams']

                self.clog.warning('ErrorMsg:{0} - ErrorRouteData:{1}'.format(msg, routedata))

                item['DataTime'] = response.meta['datatime']
                item['ErrorMsg'] = msg
                item['ErrorRouteData'] = routedata

                yield item
            except Exception as e:
                self.clog.error('errormsg is not None,ErrorType:{0},Error:{1}'.format(type(e),e))


