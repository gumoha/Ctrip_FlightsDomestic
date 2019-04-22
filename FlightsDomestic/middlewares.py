# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random,requests,json,logging,time
from scrapy.http import HtmlResponse as Response
from datetime import datetime
from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError


class FlightsdomesticSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class FlightsdomesticDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class FKRandomUserAgentMiddleware(object):
    def __init__(self):
        try:
            self.ua = UserAgent()
        except FakeUserAgentError:
            pass

    def process_request(self,request,spider):
        try:
            random_ua = self.ua.random
            request.headers['User-Agent'] = random_ua
            #spider.clog.info('User-Agent:{0}'.format(request.headers['User-Agent']))
        except Exception as e:
            spider.clog.error('FKRandomUserAgentMiddleware -- ErrorType:{0},Error:{1}'.format(type(e),e))


class PayloadRequestMiddleware(object):
    def __init__(self):
        self.filen_proxy = r'/media/gumoha/资料/Scrapy/IP_jiangxianli/freeip-DataJson/-RedisProxyData-.json'

        self.ips = self.get_IPdata()

    def get_IPdata(self):
        ips_list = []
        try:
            print('===Open File===\n')
            with open(self.filen_proxy, 'r') as f:
                dataIP = f.readlines()
                for i in dataIP:
                    try:
                        ip = json.loads(i)
                        ips_list.append(ip)
                    except Exception as e:
                        print('IP -- ErrorType:{0},Error:{1}'.format(type(e), e))
        except Exception as e:
            print('Open File -- ErrorType:{0},Error:{1}'.format(type(e), e))

        return (ips_list)


    def process_request(self,request,spider):
        if request.meta['payloadFlag'] is True:
            postUrl = request.url
            postHeaders = request.meta['payloadHeaders']
            payloadData = request.meta['payloadData']

            testnum = 0

            while testnum <= 20:

                ips = random.choice(self.ips)
                ip = {'{0}'.format(ips['protocol']): '{0}:{1}'.format(ips['ip'], ips['port'])}

                testnum +=1

                try:
                    time.sleep(random.random()*5)
                    req = requests.post(postUrl, headers=postHeaders, json=payloadData,
                                        proxies = ip,
                                        allow_redirects=False, timeout=6)
                    req.encoding = 'utf-8'
                    spider.clog.info('PayloadRequestMiddleware-Requests- UA:{0}, IP:{1}, testnum:{2}'.format(request.headers['User-Agent'],ip,testnum))
                except Exception as e:
                    spider.clog.error('PayloadRequestMiddleware-RequestsError- ErrorType:{0}, Error:{1}\n UA:{2}, IP:{3}, testnum:{4}\n'.format(type(e),e,request.headers['User-Agent'],ip,testnum))

                try:
                    plain_text = req.json()
                    errormsg = plain_text['data']['error']
                    spider.clog.warning('errormsg:{0}'.format(errormsg))
                except Exception as e:
                    spider.clog.error('errormsg Error:{0}'.format(e))



                if (req.status_code == requests.codes.ok) and (errormsg is None):
                    break
                elif testnum <= 20:
                    continue
                elif testnum > 20:
                    spider.clog.error('Testnum > 20,Break!\n')
                    break

            if (testnum <=20):
                response = Response(url=req.url, status=req.status_code,
                                    encoding=request.encoding, request=request,
                                    body=req.content)

                return response
            else:
                return None


class ProxyMiddleware(object):
    def __init__(self):
        pass

    def process_request(self,request,spider):
        try:
            request.meta['Proxy'] = None
            spider.clog.info('Proxy:{0}'.format(request.meta['Proxy']))
        except Exception as e:
            spider.clog.error('ProxyMiddleware -- ErrorType:{0},Error:{1}'.format(type(e),e))