import scrapy

class YelpSpider(scrapy.Spider):
    name = 'scrape_yelp'

    custom_settings = {
        # "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    } 
    start_urls = ['https://www.yelp.com/search?find_desc=Restaurants&find_loc=Brooklyn%2C+NY']

    def parse(self, response):
        # Extract the links to the individual restaunant
        static_yelp_url = 'https://www.yelp.com'

        for href in response.xpath('//h3/span/a/@href').extract():
            href = static_yelp_url + href
            yield scrapy.Request(
                url=href, callback=self.parse_yelp,
                meta={'url':href})
        
        # Follow pagination links and repeat
        next_url = response.xpath('//a[@class="u-decoration-none next pagination-links_anchor"]/@href').extract()[0]
        next_url = static_yelp_url + next_url
        yield scrapy.Request(url=next_url,callback=self.parse)

    def parse_yelp(self,response): 
        url = response.request.meta['url']
        try:
            name = response.xpath('//h1[@class="biz-page-title embossed-text-white shortenough"]/text()').extract()[0].strip()
        except:
            name = None
        try:
            rating = response.xpath('//div[@class="biz-rating biz-rating-very-large clearfix"]/div/@title').extract()[0].strip()
        except:
            rating = None
        try:
            address = response.xpath('//strong[@class="street-address"]/address/text()').extract()[0].strip()
        except:
            address = None
        try:
            review_count = response.xpath('//span[@class="review-count rating-qualifier"]/text()').extract()[0].strip()
        except:
            review_count = None
        try:
            transit = response.xpath('//b[@class="transit-line inline-block"]/text()').extract().strip()
        except:
            transit = None
        try:
            category = response.xpath('//span[@class="category-str-list"]/a/text()').extract()
            if len(category)%2 == 0:
                idx = len(category)/2
            else:
                idx = (len(category)/2)+1
            category = category[:idx]
        except:
            category = None
        try:
            price_range = response.xpath('//span[@class="business-attribute price-range"]/text()').extract()[0]
        except:
            price_range = None
        try:
            hours = response.xpath('//table[@class="table table-simple hours-table"]/tbody/tr').extract()
        except:
            hours = None
        try:
            price_desc = response.xpath('//dd[@class="nowrap price-description"]/text()').extract()[0].strip()
        except:
            price_desc = None
        try:
            attribute_answers = response.xpath('//dt[@class="attribute-key"]/../dd').extract()[2:].strip()
        except:
            attribute_answers = None
        try:
            attribute_key = response.xpath('//dt[@class="attribute-key"]').extract()[2:].strip()
        except:
            attribute_key = None
        yield{
        'url': url,
        'name': name,
        'rating': rating,
        'address': address,
        'review_count': review_count,
        'transit': transit,
        'category': category,
        'price_range': price_range,
        'hours': hours,
        'price_desc': price_desc,
        'attribute_key': attribute_key,
        'attribute_answers': attribute_answers
        }
