from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# time when scraping started
start = time.time()

# Flag for links limit
limitLinks = True

# Initialization of DataFrame for data storage
books_df = pd.DataFrame(
    {'book_name': [], 'type': [], 'pages_num': [], 'rating': []})

# Init:
gecko_path = '/opt/homebrew/bin/geckodriver'
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
#options.add_argument("--headless")
options.headless = False
driver = webdriver.Firefox(options=options, service=ser)

#URLs for scraping. Subpages are in code since they aren't static on webpage
url = 'https://lubimyczytac.pl/top100'
urls = ['https://lubimyczytac.pl/top100?page=1&listId=listTop100&month=5&year=2023&paginatorType=Standard',
        'https://lubimyczytac.pl/top100?page=2&listId=listTop100&month=5&year=2023&paginatorType=Standard',
        'https://lubimyczytac.pl/top100?page=3&listId=listTop100&month=5&year=2023&paginatorType=Standard',
        'https://lubimyczytac.pl/top100?page=4&listId=listTop100&month=5&year=2023&paginatorType=Standard',
        'https://lubimyczytac.pl/top100?page=5&listId=listTop100&month=5&year=2023&paginatorType=Standard',
        'https://lubimyczytac.pl/top100?page=6&listId=listTop100&month=5&year=2023&paginatorType=Standard',
        'https://lubimyczytac.pl/top100?page=7&listId=listTop100&month=5&year=2023&paginatorType=Standard']


driver.get(url)

# Check how many pages there is. If limit is TRUE then set number of pages to scrap to 5. (5x20 books = 100)
num_of_next_pages = len(urls)
if limitLinks:
    num_of_next_pages = 5
page_num = 0 # page counter

# while loop that loops through subpages of books ranking
while num_of_next_pages > page_num:
    # get subpage
    driver.get(urls[page_num])
    # Find all the links to books on subpage
    books_links = driver.find_elements(By.CLASS_NAME, 'authorAllBooks__singleTextTitle')
    # Get all the found links
    books_links_hrefs = [link.get_attribute('href') for link in books_links]

    #Loop through links
    for url2 in books_links_hrefs:
        # Get book page
        driver.get(url2)
        # Get book name
        book_name = driver.find_element(By.XPATH, '//*[@id="book-info"]/div/h1').text
        # Get type of book
        book_type = driver.find_element(By.XPATH, '//*[@id="container-book"]/div/div[2]/div[1]/div[2]/a').text
        #If number of pages exists for that book - get it
        if len(driver.find_elements(By.XPATH, '//*[@id="container-book"]/div/div[2]/div[1]/div[2]/div[3]/span[1]')) > 0:
            pages_num = driver.find_element(By.XPATH,
                                            '//*[@id="container-book"]/div/div[2]/div[1]/div[2]/div[3]/span[1]').text
        # Get book rating
        rating = driver.find_element(By.XPATH,
                                     '/html/body/div[5]/main/div/section[1]/div/div[3]/section[1]/div[1]/div[1]/span').text

        # Create vector of values and append it to DataFrame
        # Replace specific characters in num of pages and rating to create numeric variables
        book_info = {'book_name': book_name, 'type': book_type, 'pages_num': int(pages_num.replace('str.', '')),
                     'rating': float(rating.replace(',', '.'))}
        books_df = books_df._append(book_info, ignore_index=True)
    # Increment subpage counter
    page_num = page_num + 1

# Quit driver
driver.quit()

# time when scraping stopped
end = time.time()

# print performance measure
print("Selenium time:", end - start, "s")

# Data analysis

type_avgPages = books_df.groupby('type')['pages_num'].mean()
type_avgRating = books_df.groupby('type')['rating'].mean()
print("Average page number per book type: ", type_avgPages)
print("Average rating per book type:", type_avgRating)

count_type = books_df.groupby('type')['type'].count()
print("Number of books in top100 per book type", count_type)
