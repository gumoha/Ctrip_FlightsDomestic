# -*- coding: utf-8 -*-

# Scrapy settings for FlightsDomestic project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'FlightsDomestic'

SPIDER_MODULES = ['FlightsDomestic.spiders']
NEWSPIDER_MODULE = 'FlightsDomestic.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'FlightsDomestic (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'FlightsDomestic.middlewares.FlightsdomesticSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'FlightsDomestic.middlewares.FlightsdomesticDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'FlightsDomestic.pipelines.FlightsdomesticPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

ITEM_PIPELINES = {
    'FlightsDomestic.pipelines.FlightsdomesticPipeline': 300,
    #'scrapy_redis.pipelines.RedisPipeline': 400,
    'FlightsDomestic.pipelines.RedisPipeline': 500,
}


DOWNLOADER_MIDDLEWARES = {
    'FlightsDomestic.middlewares.FKRandomUserAgentMiddleware': 10,
    #'FlightsDomestic.middlewares.ProxyMiddleware':100,
    'FlightsDomestic.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'FlightsDomestic.middlewares.PayloadRequestMiddleware':20,
}

DOWNLOAD_TIMEOUT = 120

DOWNLOAD_DELAY=1.25
#CLOSESPIDER_ITEMCOUNT =

FEED_EXPORT_ENCODING = 'utf-8'

#配置redis
#SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
#DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
#REDIS_URL = 'redis://127.0.0.1:6379'

#REDIS_START_URLS_AS_SET = False
#REDIS_START_URLS_KEY = '%(name)s:start_urls'

#REDIS_ITEMS_KEY = '%(spider)s:items'
#REDIS_ITEMS_SERIALIZER = 'json.dumps'