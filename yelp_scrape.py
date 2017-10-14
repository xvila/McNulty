import scrapy

class MovieSpider(scrapy.Spider):
    name = 'scrape_yelp'

    custom_settings = {
        # "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    } 
    start_urls = ['https://www.yelp.com/search?find_desc=Restaurants&find_loc=Brooklyn%2C+NY']
    
    # for i in range(1970,2016):
    #     #base = 'http://www.imdb.com/search/title?release_date={}'
    #     base = 'http://www.imdb.com/search/title?year={},{}&title_type=feature&sort=moviemeter,asc'
    #     url = base.format(i,i)
    #     start_urls.append(url)

    def parse(self, response):
        # Extract the links to the individual movie
        static_yelp_url = 'https://www.yelp.com'
        #static_list_url = 'http://www.imdb.com/search/title'

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
            name = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract()[0].strip()
        except:
            name = None
        try:
            budget = response.xpath('//div[@class="txt-block"]/h4/text()[contains(.,"Budget")]/../../text()').extract()[1].strip()
        except:
            budget = None
        try:
            box_office = response.xpath('//div[@class="txt-block"]/h4/text()[contains(.,"Gross")]/../../text()').extract()[1].strip()
        except:
            box_office = None
        try:
            release_date = response.xpath('//div[@class="txt-block"]/h4/text()[contains(.,"Release Date:")]/../../text()').extract()[1].strip()
        except:
            release_date = None
        try:
            user_rating = response.xpath('//div[@class="ratingValue"]//span/text()').extract()[0]
        except:
            user_rating = None
        try:
            genre = response.xpath('//div[@itemprop="genre"]/a/text()').extract()
        except:
            genre = None
        try:
            year = response.xpath('//span[@id="titleYear"]/a/text()').extract()[0]
        except:
            year = None
        try:
            rating = response.xpath('//meta[@itemprop="contentRating"]/../text()').extract()[1].strip()
        except:
            rating = None
        try:
            runtime = response.xpath('//div[@class="txt-block"]/time/text()').extract()[0]
        except:
            runtime = None
        try:
            director = response.xpath('//span[@itemprop="director"]/a/span/text()').extract()[0]
        except:
            director = None
     
        yield{
        'url': url,
        'name': name,
        'budget': budget,
        'box_office': box_office,
        'user_rating': user_rating,
        'genre': genre,
        'year': year,
        'rating': rating,
        'runtime': runtime,
        'director': director,
        'release_date': release_date
        }
