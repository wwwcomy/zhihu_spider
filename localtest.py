import os
from bs4 import BeautifulSoup
import re
from scrapy_1.models.model import CrawlSummary
from scrapy_1.dao.sqlite_dao import SqliteCrawSummaryDao
from datetime import datetime


file = open("teacher.html", 'r')
html_doc = file.read()
soup = BeautifulSoup(html_doc, 'html.parser')
# This is for the district
# rs = soup.select('div[data-role="ershoufang"] a')
# for i in range(0, len(rs)):
#     print(rs[i])

# this is title
title = soup.select('div.info div.title a')[0].get_text()
position_id = soup.select('li.clear.LOGVIEWDATA.LOGCLICKDATA')[0].get('data-lj_action_resblock_id')
position_info = soup.select('div.info div.positionInfo a')[0].get_text()
house_id = soup.select('li.clear.LOGVIEWDATA.LOGCLICKDATA')[0].get('data-lj_action_housedel_id')
house_info = soup.select('div.info div.houseInfo')[0].get_text().replace('\n','').replace(' ','')
split_house_info = house_info.replace(' ', '').replace('\n','').split('|')
house_type = split_house_info[0]
house_area = split_house_info[1]
house_direction = split_house_info[2]
house_decoration = split_house_info[3]
house_floor = split_house_info[4]
house_year = split_house_info[5]

total_price = soup.select('div.info div.totalPrice span')[0].get_text()
unit_price_raw = soup.select('div.info div.unitPrice span')[0].get_text()
unit_price = re.sub('[^\d\\.]','',unit_price_raw)

print(f'title: {title}')
print(f'position_id: {position_id}')
print(f'position_info: {position_info}')
print(f'house_id: {house_id}')
print(f'house_info: {house_info}')
print(f'house_type: {house_type}')
print(f'house_area: {house_area}')
print(f'house_direction: {house_direction}')
print(f'house_decoration: {house_decoration}')
print(f'house_floor: {house_floor}')
print(f'house_year: {house_year}')
print(f'total_price: {total_price}')
print(f'unit_price: {unit_price}')


curr_datetime = datetime.now()
curr_date = curr_datetime.date()
crawl_summary = CrawlSummary(1, 'test', curr_date, curr_datetime, curr_datetime, 100)
summary_dao = SqliteCrawSummaryDao()
summary_dao.save_craw_summary(crawl_summary)