import scrapy


class EgteaSpiderSpider(scrapy.Spider):
    name = "egtea_spider"
    allowed_domains = ["cbs.ic.gatech.edu"]
    start_urls = ["https://cbs.ic.gatech.edu/fpv/"]

    def parse(self, response):
        for div in response.css('div.one'):
            button_reference = div.css('h2::text').get().strip()
            links = div.css('a::attr(href)').getall()
            for link in links:
                yield {button_reference: link}

        for a_tag in response.css('div.releases ul a'):
            link = a_tag.attrib['href']
            description = a_tag.css('b::text').get().strip()
            yield {description: link}