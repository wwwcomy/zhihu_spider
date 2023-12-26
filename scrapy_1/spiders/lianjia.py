import scrapy
import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy_1.constants import LIANJIA_HEADER
from bs4 import BeautifulSoup


FOLDER = '/Users/xingnliu/tmp1/lianjia/'

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["sh.lianjia.com"]
    start_urls = ["https://sh.lianjia.com/ershoufang/minhang/co32/"]

    sub_district_set = set()


    # def start_requests(self):
    #     urls = [
    #         'https://sh.lianjia.com/ershoufang/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse_index_page, headers=LIANJIA_HEADER)

    def parse(self, response):
        district_anchor_href = response.css('div[data-role="ershoufang"] div:nth-child(1) a::attr(href)').getall()
        district_anchor_content = response.css('div[data-role="ershoufang"] div:nth-child(1) a::text').getall()

        # sub_district_anchor_href = response.css('div[data-role="ershoufang"] div:nth-child(2) a::attr(href)').getall()
        # sub_district_anchor_content = response.css('div[data-role="ershoufang"] div:nth-child(2) a::text').getall()
        for i in range(0, len(district_anchor_href)):
            print(f'Fetching sub district for {district_anchor_content[i]}')
            url = f'https://sh.lianjia.com{district_anchor_href[i]}'
            yield scrapy.Request(url=url, callback=self.parse_sub_district, headers=LIANJIA_HEADER, cb_kwargs=dict(district=district_anchor_content[i]))

    def parse_sub_district(self, response, district):
        sub_district_anchor_hrefs = response.css('div[data-role="ershoufang"] div:nth-child(2) a::attr(href)').getall()
        sub_district_anchor_contents = response.css('div[data-role="ershoufang"] div:nth-child(2) a::text').getall()
        

        for i in range(0, len(sub_district_anchor_hrefs)):
            print(f'Parsing sub district {sub_district_anchor_contents} for {district}')
            sub_district_anchor_content = sub_district_anchor_contents[i]
            if sub_district_anchor_content in self.district_set:
                print(f'Sub district {sub_district_anchor_content} already parsed')
                continue
            self.sub_district_set.add(sub_district_anchor_content)
            url = f'https://sh.lianjia.com{sub_district_anchor_hrefs[i]}'
            yield scrapy.Request(url=url, callback=self.parse_index_page, headers=LIANJIA_HEADER, 
                                 cb_kwargs=dict(district=district, sub_district=sub_district_anchor_content))

    def parse_index_page(self, response, district_dict):
        district = district_dict.get('district')
        sub_district = district_dict.get('sub_district')
        house_list = response.css('ul.sellListContent li.cli').getall()
        for house_li_content in house_list:
            soup = BeautifulSoup(house_li_content, 'html.parser')
            title = soup.select('div.title a')[0].get_text()
            
        # next_page_href = response.css('div.page-box.house-lst-page-box a.internal::attr(href)').getall()
        # next_page_text = response.css('div.RichText a.internal::text').getall()
        # if next_page_text is not None:
        #     for i in range(0, len(next_page_text)):
        #         text = next_page_text[i]
        #         if text.find('英语') == -1:
        #             continue
        #         # yield response.follow(next_page_href[i], callback=self.parse)
        #         url = next_page_href[i]
        #         yield scrapy.Request(url=url, callback=self.parse_pic, headers=LIANJIA_HEADER)


# process = CrawlerProcess(settings={
#     "DOWNLOAD_DELAY": 10,
#     "COOKIES_ENABLED": False,
#     "DEPTH_PRIORITY": 2,
# })

# process.crawl(LianjiaSpider)
# process.start()  # the script will block here until the crawling is finished
# process.join()
