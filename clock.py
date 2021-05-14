from apscheduler.schedulers.blocking import BlockingScheduler
import newsScraper.spiders.businessSpider as newsSpider
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

configure_logging()
runner = CrawlerRunner(get_project_settings())
sched = BlockingScheduler()
job_defaults = {
        'coalesce': False,
        'max_instances': 3
}
sched.configure(job_defaults=job_defaults)


def crawl():
    runner.crawl(newsSpider.BusinessspiderSpider)
    if not reactor.running:
        reactor.run(installSignalHandlers=0)  # the script will block here until all crawling jobs are finished
    else:
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())


@sched.scheduled_job('interval', hours=3)
def timed_job():
    crawl()


sched.start()
