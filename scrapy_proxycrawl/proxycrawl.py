import urllib
import logging

log = logging.getLogger('scrapy.proxycrawl')

class ProxyCrawlMiddleware(object):
    def __init__(self, settings):
        self.proxycrawl_enabled = settings.get('PROXYCRAWL_ENABLED', True)
        self.proxycrawl_token = settings.get('PROXYCRAWL_TOKEN')
        self.proxycrawl_url = 'https://api.proxycrawl.com'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if not self.proxycrawl_enabled:
            log.warning('Skipping ProxyCrawl API CALL disabled!')
            return
        if self.proxycrawl_url not in request.url:
            new_url = 'https://api.proxycrawl.com/?token=%s&url=%s' % (self.proxycrawl_token, urllib.quote(request.url))
            log.debug('Using ProxyCrawl API, overridden URL is: %s' % (new_url))
            return request.replace(url=new_url)
