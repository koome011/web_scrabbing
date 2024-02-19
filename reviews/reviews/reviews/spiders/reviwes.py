import scrapy
import re
from ..items import ReviewsItem
from scrapy.http import Request

class ReviewsSpider(scrapy.Spider):
    name = 'reviwes'
    page_number = 2
    start_urls = [
        'https://www.jumia.co.ke/catalog/productratingsreviews/sku/SK493EA06FGSGNAFAMZ/'
    ]

    def parse(self, response):

        items = ReviewsItem()

        all_reviews = response.css('article.-pvs')

        for review in all_reviews:
            client_text = review.css('div.-pvs span:nth-child(2)::text').extract_first()
            # Remove "By" prefix using string manipulation:
            name = client_text.lstrip("by ").strip()  # Handles both "By " and " By" cases

            rating = review.css('div.stars::text').extract_first()
            rating = re.search(r'\d+', rating).group()

            summary = review.css('h3.-m::text').extract_first()
            text = review.css('p.-pvs::text').extract_first()

            items['name'] = name
            items['rating'] = rating
            items['summary'] = summary
            items['text'] = text
            yield items

        # Increment the page number
        next_page = f"https://www.jumia.co.ke/catalog/productratingsreviews/sku/SK493EA06FGSGNAFAMZ/?page={self.page_number}"
        self.page_number += 1

        yield Request(next_page, callback=self.parse)


        # Check if we've reached the maximum page number
        # if self.page_number <= 18:
        #     # Follow the next page link
        #     yield Request(next_page, callback=self.parse)