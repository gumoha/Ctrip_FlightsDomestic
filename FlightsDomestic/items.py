# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FlightsdomesticItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    DataTime = scrapy.Field()  # 查询日期时间

    RouteData = scrapy.Field()

    RouteCount = scrapy.Field()
    RouteType = scrapy.Field()  # 路线类型（直飞，转达）

    LegType = scrapy.Field()

    FlightID = scrapy.Field()  # 网站航班唯一编号
    FlightNumber = scrapy.Field()  # 航空公司航班号

    AirlineName = scrapy.Field()  # 航空公司
    AirlineCode = scrapy.Field()  # 航空公司代码
    SharedFlightNumber = scrapy.Field()
    SharedFlightName = scrapy.Field()

    CraftTypeName = scrapy.Field()  # 机型名字
    CraftKind = scrapy.Field()  # 飞机类型（
    CraftTypeCode = scrapy.Field()
    CraftTypeKindDisplayName = scrapy.Field()

    PunctualityRate = scrapy.Field()  # 准点率
    MealType = scrapy.Field()  # 机餐

    DepartureDate = scrapy.Field()  # 出发时间
    DepartureAirportID = scrapy.Field()  # 出发机场
    DepartureAirportName = scrapy.Field()  # 出发航站楼
    DepartureCityTlc = scrapy.Field()
    DepartureCityName = scrapy.Field()

    ArrivalDate = scrapy.Field()  # 抵达时间
    ArrivalAirportID = scrapy.Field()  # 抵达机场
    ArrivalAirportName = scrapy.Field()  # 抵达航站楼
    ArrivalCityTlc = scrapy.Field()
    ArrivalCityName = scrapy.Field()

    Cabins = scrapy.Field()  # 价格，飞机舱位，折扣
    CabinsCount = scrapy.Field()

    ErrorMsg = scrapy.Field()
    ErrorRouteData = scrapy.Field()
