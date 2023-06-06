import scrapy

class Books(scrapy.Item):
    book_name        = scrapy.Field()
    type             = scrapy.Field()
    pages_num        = scrapy.Field()
    rating           = scrapy.Field()

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['lubimyczytac.pl']
    try:
        with open("links_list_books.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    def parse(self, response):
        p = Books()

        book_name_xpath        = '//*[@class="book__title"]/text()'
        type_xpath             = '//*[@class="book__category d-sm-block d-none"]/text()'
        pages_num_xpath        = '//*[@class="d-sm-inline-block book-pages book__pages pr-2 mr-2 pr-sm-3 mr-sm-3"]/text()'
        rating_xpath           = '//*[@id="container-book"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/span[2]/text()'

        p['book_name']         = response.xpath(book_name_xpath).getall()
        p['type']              = response.xpath(type_xpath).getall()
        p['pages_num']         = response.xpath(pages_num_xpath).getall()
        p['rating']            = response.xpath(rating_xpath).getall()

        yield p
