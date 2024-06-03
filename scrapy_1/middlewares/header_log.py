from scrapy import signals

class HttpHeaderLoggingMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Log the request headers
        spider.logger.debug(f"Request Headers: {request.headers.to_unicode_dict()}")

    def process_response(self, request, response, spider):
        # Log the response headers
        spider.logger.debug(f"Response Headers: {response.headers.to_unicode_dict()}")
        return response

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)