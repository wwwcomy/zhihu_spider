import scrapy
from scrapy_1.constants import LIANJIA_HEADER
from bs4 import BeautifulSoup
from scrapy_1.models.model import CrawlSummary
from datetime import datetime
from scrapy_1.dao.sqlite_dao import SqliteCrawSummaryDao, SqliteHouseInfoDao, HousePriceChangeHistoryDao
from scrapy_1.models.model import HouseInfo
from scrapy import signals
import json
from pydispatch import dispatcher
import re


FOLDER = '/Users/xingnliu/tmp1/lianjia/'

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["sh.lianjia.com"]
    start_urls = ["https://sh.lianjia.com/ershoufang/minhang/co32/"]

    sub_district_set = set()

    def __init__(self):
        self.job_start_time = datetime.now()
        self.job_start_date = self.job_start_time.date()
        self.data_count = 0
        self.new_data_count = 0
        self.price_higher_count = 0
        self.price_lower_count = 0
        print(f'job start date: {self.job_start_date}')
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        print('spider closed, processing post job...')
        curr_datetime = datetime.now()
        job_summary = CrawlSummary(None, 'lianjia', self.job_start_date, self.job_start_time, curr_datetime, self.data_count,
                                   self.new_data_count, self.price_higher_count, self.price_lower_count)
        SqliteCrawSummaryDao().save_craw_summary(job_summary)


    def parse(self, response):
        district_anchor_href = response.css('div[data-role="ershoufang"] div:nth-child(1) a::attr(href)').getall()
        district_anchor_content = response.css('div[data-role="ershoufang"] div:nth-child(1) a::text').getall()

        for i in range(0, len(district_anchor_href)):
            print(f'Fetching sub district for {district_anchor_content[i]}')
            url = f'https://sh.lianjia.com{district_anchor_href[i]}'
            yield scrapy.Request(url=url, callback=self.parse_sub_district, headers=LIANJIA_HEADER, cb_kwargs=dict(district=district_anchor_content[i]))

    def parse_sub_district(self, response, district):
        sub_district_anchor_hrefs = response.css('div[data-role="ershoufang"] div:nth-child(2) a::attr(href)').getall()
        sub_district_anchor_contents = response.css('div[data-role="ershoufang"] div:nth-child(2) a::text').getall()

        for i in range(0, len(sub_district_anchor_hrefs)):
            sub_district_anchor_content = sub_district_anchor_contents[i]
            sub_district_anchor_href = sub_district_anchor_hrefs[i]
            print(f'Parsing sub district {sub_district_anchor_content} for {district}')
            if sub_district_anchor_content in self.sub_district_set:
                print(f'Sub district {sub_district_anchor_content} already parsed')
                continue
            self.sub_district_set.add(sub_district_anchor_content)
            url = f'https://sh.lianjia.com{sub_district_anchor_href}'
            yield scrapy.Request(url=url, callback=self.parse_houses, headers=LIANJIA_HEADER, 
                                 cb_kwargs=dict(district=district, sub_district=sub_district_anchor_content, start_page = True))

    def parse_houses(self, response, district, sub_district, start_page=False):
        house_list = response.css('ul.sellListContent li.clear.LOGVIEWDATA.LOGCLICKDATA').getall()
        for house_li_content in house_list:
            house_info = self.extract_house_info(house_li_content, district, sub_district)
            self.process_house_info(house_info)
        if not start_page:
            return
        page_info = response.css('div.page-box.house-lst-page-box::attr(page-data)').getall()
        if len(page_info) == 0:
            print(f'No page info found for {district} {sub_district}')
            return
        total_page = json.loads(page_info[0])['totalPage']
        page_url_raw = response.css('div.page-box.house-lst-page-box::attr(page-url)').getall()[0]
        for i in range(2, total_page+1):
            page_url = page_url_raw.format(page=i)
            if not page_url.endswith('/'):
                page_url = page_url + '/'
            url = f'https://sh.lianjia.com{page_url}'
            yield scrapy.Request(url=url, callback=self.parse_houses, headers=LIANJIA_HEADER,
                                 cb_kwargs=dict(district=district, sub_district=sub_district))

    def extract_house_info(self, house_li_content, district, sub_district) -> HouseInfo:
        soup = BeautifulSoup(house_li_content, 'html.parser')
        title = soup.select('div.info div.title a')[0].get_text()
        position_id = soup.select('li.clear.LOGVIEWDATA.LOGCLICKDATA')[0].get('data-lj_action_resblock_id')
        position_info = soup.select('div.info div.positionInfo a')[0].get_text()
        house_id = soup.select('li.clear.LOGVIEWDATA.LOGCLICKDATA')[0].get('data-lj_action_housedel_id')
        house_info = soup.select('div.info div.houseInfo')[0].get_text().replace('\n','').replace(' ','')
        split_house_info = house_info.replace(' ', '').replace('\n','').split('|')
        house_type = split_house_info[0]
        house_area = split_house_info[1]
        house_area = re.sub('[^\d\\.]','',house_area)
        house_direction = split_house_info[2]
        house_decoration = split_house_info[3]
        house_floor = split_house_info[4]
        house_year = split_house_info[5]

        total_price = soup.select('div.info div.totalPrice span')[0].get_text()
        unit_price_raw = soup.select('div.info div.unitPrice span')[0].get_text()
        unit_price = re.sub('[^\d\\.]','',unit_price_raw)
        house_info_entity = HouseInfo(None, house_id, district, sub_district, title, position_id, position_info,
                                      house_info, house_type, house_area, house_direction, house_decoration,
                                      house_floor, house_year, total_price, unit_price, self.job_start_date)
        return house_info_entity
    
    def process_house_info(self, house_info: HouseInfo):
        house_info_dao = SqliteHouseInfoDao()
        self.data_count += 1
        existing_house_info = house_info_dao.get_house_info(house_info.house_id)
        if existing_house_info is None:
            house_info_dao.save_house_info(house_info)
            self.new_data_count += 1
            return
        # if there's existing info, check if there's any price change
        house_change_history = existing_house_info.generate_price_change_history(house_info, self.job_start_date)
        if house_change_history is None:
            if existing_house_info.last_update_date == self.job_start_date:
                # already processed, skip
                return
            house_info_dao.update_last_update_date(existing_house_info, self.job_start_date)
            return
        if house_change_history.change_type == 'down':
            # price down, update the history
            self.price_lower_count += 1
        else:
            # price up, update the history
            self.price_higher_count += 1
        # house_info should have the same id as existing_house_info, so we can use it to update price
        house_info_dao.update_house_price(house_info, self.job_start_date)
        HousePriceChangeHistoryDao().save_house_price_change_history(house_change_history)
        return


