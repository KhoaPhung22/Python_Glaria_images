import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin

class GlamiraSpider(scrapy.Spider):
    name = 'glamiraspider'
    start_urls = ['https://www.glamira.com']

    custom_settings = {
        'FEEDS': {
            'images.json': {'format': 'json'},
        },
    }

    def __init__(self):
        self.visited_urls = set()  # Set to track visited image URLs

    def parse(self, response):
        # Extract image URLs
        for img in response.css('img::attr(src)').getall():
            img_url = urljoin(response.url, img)
            if img_url not in self.visited_urls:
                self.visited_urls.add(img_url)
                yield {'image_url': img_url}

        for source in response.css('source::attr(srcset)').getall():
            source_url = urljoin(response.url, source)
            if source_url not in self.visited_urls:
                self.visited_urls.add(source_url)
                yield {'image_url': source_url}

        # Follow links to other pages
        for next_page in response.css('a::attr(href)').getall():
            next_page_url = urljoin(response.url, next_page)
            if 'glamira.com' in next_page_url:  # Ensure it stays within the domain
                yield response.follow(next_page_url, self.parse)

# Running the spider
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(GlamiraSpider)
    process.start()