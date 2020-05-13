#import urlparse
import os
import scrapy

from scrapy.http import Request


class springerSpider(scrapy.Spider):
    name = "springer"
    allowed_domains = ["link.springer.com"]
    start_urls = [
                 "https://link.springer.com/search/page/1?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/2?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/3?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/4?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/5?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/6?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/7?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/8?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/9?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/10?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/11?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/12?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/13?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/14?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/15?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/16?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/17?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/18?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/19?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false",
                 "https://link.springer.com/search/page/20?facet-content-type=%22Book%22&package=mat-covid19_textbooks&showAll=false"
]

    def parse(self, response):
        for href in response.css('ol#results-list a[href*=book]::attr(href)').extract():
            yield Request(
            url=response.urljoin(href),
            callback=self.parse_book
            )

    def parse_book(self, response):
        href = response.css('a[title*=Download][href$=".pdf"]::attr(href)').extract_first()
        book_title = response.css('h1::text').extract_first()
        yield Request(
            url=response.urljoin(href),
            callback=self.save_pdf,
            meta={'book_title': book_title}
            )

    def save_pdf(self, response):
        book_title = response.meta.get('book_title')
        book_title = book_title.replace("!@#$%^&*()[]{};:,./<>?\|`~-=_+", "")
        book_title = book_title.replace(" ", "_")
        self.logger.info('Saving PDF %s', book_title + ".pdf")
        if os.path.exists(os.getcwd() + "/" + book_title + ".pdf"):
           self.logger.info ("Archivo existe")
           pass
        else:
           with open(book_title + ".pdf", 'wb') as f:
                f.write(response.body)
