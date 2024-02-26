import scrapy


class EgteaSpiderSpider(scrapy.Spider):
    name = "egtea_spider"
    allowed_domains = ["cbs.ic.gatech.edu"]
    start_urls = ["https://cbs.ic.gatech.edu/fpv/"]

    def parse(self, response):
        for div_section in response.xpath('//div[@class="one"]'):
            links = div_section.xpath('.//a')
            for link in links:
                link_text = link.xpath('text()').get().strip()
                link_href = link.xpath('@href').get()
                yield {link_text: link_href}

        for a_tag in response.css('div.releases ul a'):
            link = a_tag.attrib['href']
            description = a_tag.css('b::text').get().strip()
            yield {description: link}