import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()

class LinksListBooksSpider(scrapy.Spider):
    name = 'links_list_books'
    allowed_domains = ['lubimyczytac.pl']
    start_urls = ['https://lubimyczytac.pl/top100',
                  'https://lubimyczytac.pl/top100?page=2&listId=listTop100&month=5&year=2023&paginatorType=Standard',
                  'https://lubimyczytac.pl/top100?page=3&listId=listTop100&month=5&year=2023&paginatorType=Standard',
                  'https://lubimyczytac.pl/top100?page=4&listId=listTop100&month=5&year=2023&paginatorType=Standard',
                  'https://lubimyczytac.pl/top100?page=5&listId=listTop100&month=5&year=2023&paginatorType=Standard',
                  'https://lubimyczytac.pl/top100?page=6&listId=listTop100&month=5&year=2023&paginatorType=Standard',
                  'https://lubimyczytac.pl/top100?page=7&listId=listTop100&month=5&year=2023&paginatorType=Standard']

    def parse(self, response):
        xpath = '//*[@class="authorAllBooks__singleTextTitle float-left"]//@href'
         
        selection = response.xpath(xpath)

        for s in selection:
            l = Link()
            l['link'] = 'http://lubimyczytac.pl' + s.get()
            
            yield l
