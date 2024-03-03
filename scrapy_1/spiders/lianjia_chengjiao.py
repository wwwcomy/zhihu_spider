import scrapy
from scrapy_1.constants import LIANJIA_CHENGJIAO_HEADER
from bs4 import BeautifulSoup
from scrapy_1.models.model import CrawlSummary
from datetime import datetime
from scrapy_1.dao.sqlite_dao import SqliteCrawSummaryDao, SqliteHouseInfoDao, HousePriceChangeHistoryDao
from scrapy_1.models.model import HouseInfo
from scrapy import signals
from http.cookies import SimpleCookie
import json
from pydispatch import dispatcher
import re


FOLDER = '/Users/xingnliu/tmp1/lianjia/'

class LianjiaChengjiaoSpider(scrapy.Spider):
    name = "lianjia_chengjiao"
    xiaoqu = "c5011000012246"
    raw_cookie = "CHANGE_TO_COOKIE_STRING"
    cookies = {}

    def __init__(self):
        cookie = SimpleCookie()
        cookie.load(self.raw_cookie)
        self.cookies = {k: v.value for k, v in cookie.items()}

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        print('spider closed, processing post job...')

    def start_requests(self):
        urls = [f"https://sh.lianjia.com/chengjiao/{self.xiaoqu}/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,  cookies=self.cookies)

    def parse(self, response):
        page_data = response.css('div.page-box.house-lst-page-box::attr(page-data)').get()
        total_page = json.loads(page_data)['totalPage']
        self.parse_chengjiao(response)
        for i in range(2, total_page+1):
            print(f'Fetching next page for pg{i}{self.xiaoqu}')
            url = f'https://sh.lianjia.com/chengjiao/pg{i}{self.xiaoqu}/'
            yield scrapy.Request(url=url, callback=self.parse_chengjiao,  cookies=self.cookies)
    
    def parse_chengjiao(self, response):
        house_list = response.css('ul.listContent div.info').getall()
        if len(house_list) == 0:
            print(f'No house_list info found')
            return
        for house in house_list:
            soup = BeautifulSoup(house, 'html.parser')
            title = soup.select('div.title a')[0].text
            deal_date = soup.select('div.dealDate')[0].text
            total_price = soup.select('div.totalPrice span')[0].text
            unit_price = soup.select('div.unitPrice span')[0].text
            self.append_to_file(f'chengjiao.txt', f'{title}\t{deal_date}\t{total_price}\t{unit_price}')

    def append_to_file(self, file_name, content):
        with open(file_name, 'a') as f:
            f.write(content+'\n')

