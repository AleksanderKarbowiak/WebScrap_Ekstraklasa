# WebScrap_lubimyCzytac

Running scrapy:
1. Download folder scrapy.
2. Run console command.
3. Change directory (cd command) to \lubimyczytac.
4. In order to save links to scrap run: scrapy crawl links_list_books -O links_list_books.csv.
5. The file links_list_books.csv contains links to pages the program will crawl through.
6. In order to crawl through links and save results run: scrapy crawl books -O books.csv
7. The file books.csv contains all scrapped data.
8. It is possible to change a limit of the number of pages scrapped to 100 in the file 'books.py'. To do so change assigned boolean parameter of limit_pages_100 to True.

Running selenium:
1. Install selenium and pandas.
2. Set limitLinks flag to TRUE (if you want to scrap 100 links) or FALSE (if you want to scrap all the links)
3. Run script by command line and have fun :)
