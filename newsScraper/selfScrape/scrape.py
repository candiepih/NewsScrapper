from scrapy.utils.project import get_project_settings
import newsScraper.spiders.businessSpider as newsSpider
import sys
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)


class StartScraper:
    def start(self):
        self.crawl()
        reactor.run()  # the script will block here until the last crawl call is finished

    @defer.inlineCallbacks
    def crawl(self):
        d = runner.crawl(newsSpider.BusinessspiderSpider)
        runner.join()
        d.addBoth(lambda _: reactor.stop())
        d.addErrback(self.catch_error)
        yield d

    def catch_error(self, failure):
        sys.stdout.write("An error occurred while executing crawl runner")




