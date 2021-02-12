from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
import newsScraper.spiders.businessSpider as newsSpider
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


class Command(BaseCommand):
    def handle(self, *args, **options):
        configure_logging()
        self.runner = CrawlerRunner(get_project_settings())
        self.scheduler()

    def crawl(self):
        self.runner.crawl(newsSpider.BusinessspiderSpider)
        if not reactor.running:
            reactor.run(installSignalHandlers=0)  # the script will block here until all crawling jobs are finished

    def scheduler(self):
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        scheduler = BackgroundScheduler()
        scheduler.configure(job_defaults=job_defaults)
        scheduler.add_job(self.crawl, 'interval', minutes=5)
        d = self.runner.join()
        if reactor.running:
            d.addBoth(lambda _: reactor.stop())
        scheduler.start()




