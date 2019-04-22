# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs,json,logging
from datetime import datetime
import redis


class FlightsdomesticPipeline(object):
    def __init__(self):
        self.time_now = datetime.now().strftime('%Y-%m-%d %H:%M')


    def open_spider(self,spider):
        filen = '/media/gumoha/资料/Scrapy/xiecheng_AirTicket/FlightsDomestic/DATA/{0}-({1}).json'.format('FlightsDomesticAirTicket',self.time_now)
        self.file = codecs.open(filen,'w')

    def close_spider(self,item,spider):
        self.file.close()

    def process_item(self, item, spider):
        line = '{0}\n'.format(json.dumps(dict(item),ensure_ascii=False))
        self.file.write(line)

        return item



class RedisPipeline(object):
    def open_spider(self,spider):
        try:
            pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password=None,
                                        encoding='utf-8', decode_responses=True)
            self.redisdb = redis.Redis(connection_pool=pool)
            spider.clog.info('链接Redis:{0} 成功'.format(self.redisdb))
        except Exception as e:
            spider.clog.error('链接Redis失败')

        self.item_key = 'CtripFlights_SpiderData'
        self.succeed_key = 'CtripFlights_AllCitysRouteDataSucceed'
        self.failing_key = 'CtripFlights_AllCitysRouteDataFailing'


    def close_spider(self,item,spider):
        pass

    def process_item(self,item,spider):
        #item存入Redis
        try:
            self.redisdb.sadd(self.item_key, json.dumps(dict(item)))
        except Exception as e:
            spider.clog.warning('存入失败！Redis_key:{0}\n{1}\nError:{2}\n'.format(self.item_key, dict(item), e))


        # 通航的城市数据
        if item['ErrorMsg'] is None:
            routedata = item['RouteData'][0]
            routedata['date'] = None
            try:
                self.redisdb.sadd(self.succeed_key, json.dumps(routedata))

            except Exception as e:
                spider.clog.error('存入失败！Redis_key:{0}\n{1}\nError:{2}\n'.format(self.succeed_key, str(routedata),e))
        # 不通航的城市数据
        else:
            routedata = item['ErrorRouteData'][0]
            routedata['date'] = None
            try:
                self.redisdb.sadd(self.failing_key, json.dumps(routedata))

            except Exception as e:
                spider.clog.error('存入失败！Redis_key:{0}\n{1}\nError:{2}\n'.format(self.failing_key, str(routedata),e))


        return item
