import scrapy
import os
import json
import requests
from scrapy.crawler import CrawlerProcess
from scrapy_1.constants import ZHIHU_HEADER, ZHIMG_HEADER

FOLDER = '/Users/xingnliu/tmp1/zhuanlan/'


def mkdir(path):
    whole_path = os.path.join(FOLDER, path)
    folder = os.path.exists(whole_path)
    if not folder:
        os.makedirs(whole_path)


def download_pic(title, counter, d):
    image_url = d.get("src")
    whole_path = os.path.join(FOLDER, title, '{}.jpg'.format(counter))

    if counter != -1:
        try:
            image = requests.get(image_url, headers=ZHIMG_HEADER, stream=True)
            with open(whole_path, 'wb') as img:
                img.write(image.content)
            print(f"download success to: {whole_path}")
        except Exception as exc:
            print(exc)


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"

    def start_requests(self):
        urls = [
            'https://zhuanlan.zhihu.com/p/363982330',
            # 'https://zhuanlan.zhihu.com/p/392239940',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_index_page, headers=ZHIHU_HEADER)

    def parse_index_page(self, response):
        next_page_href = response.css('div.RichText a.internal::attr(href)').getall()
        next_page_text = response.css('div.RichText a.internal::text').getall()
        if next_page_text is not None:
            for i in range(0, len(next_page_text)):
                text = next_page_text[i]
                if text.find('英语') == -1:
                    continue
                # yield response.follow(next_page_href[i], callback=self.parse)
                url = next_page_href[i]
                yield scrapy.Request(url=url, callback=self.parse_pic, headers=ZHIHU_HEADER)

    def parse_pic(self, response):
        counter = 0
        zhuanlan_name = self.get_zhuanlan_name(response)
        if not zhuanlan_name:
            return
        title = response.css('h1.Post-Title::text').get()
        mkdir(title)
        txt_path = os.path.join(FOLDER, title, "foo.txt")
        with open(txt_path, "a") as fo:
            for img in response.css('figure>img.origin_image'):
                counter = counter + 1
                if img.attrib.get('data-original'):
                    d = {
                        'src': img.attrib['data-original']
                    }
                else:
                    d = {
                        'src': img.attrib['data-actualsrc']
                    }
                fo.write(json.dumps(d) + '\n')
                download_pic(title, counter, d)
                yield d

    def get_zhuanlan_name(self, response):
        # zhuanlan_name = response.css('h2.ContentItem-title')
        # if zhuanlan_name:
        #    return zhuanlan_name.css('div div::text').get()
        zhuanlan_name = response.css('title::text')
        if zhuanlan_name:
            return zhuanlan_name.get()

    def parse2(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


# process = CrawlerProcess(settings={
#     # "FEEDS": {
#     #     "items.json": {"format": "json"},
#     # },
#     "DOWNLOAD_DELAY": 10,
#     "COOKIES_ENABLED": False,
#     "DEPTH_PRIORITY": 2,
# })

# process.crawl(ZhihuSpider)
# process.start()  # the script will block here until the crawling is finished
# process.join()
