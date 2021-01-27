from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from django.core.management.base import BaseCommand
import newsScraper.spiders.businessSpider as news_spider


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.crawl()
        reactor.run()

    @staticmethod
    def crawl_job():
        settings = get_project_settings()
        runner = CrawlerRunner(settings)
        return runner.crawl(news_spider.BusinessspiderSpider)

    def schedule_next_crawl(self, null, sleep_time):
        reactor.callLater(sleep_time, self.crawl)

    def crawl(self):
        d = self.crawl_job()
        d.addCallback(self.schedule_next_crawl, 30)
        d.addErrback(self.catch_error)

    def catch_error(self, failure):
        self.stdout.write(failure.value)



