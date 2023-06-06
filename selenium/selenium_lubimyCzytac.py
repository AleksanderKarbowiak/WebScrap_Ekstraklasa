from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
# Pressing enter:
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import getpass
import datetime

limitLinks = True

books_df = pd.DataFrame(
    {'book_name': [], 'type': [], 'pages_num': [], 'rating': []})

# Init:
gecko_path = '/opt/homebrew/bin/geckodriver'
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options=options, service=ser)

url = 'https://lubimyczytac.pl/top100'
urls = ['https://lubimyczytac.pl/top100?page=1&listId=listTop100&month=5&year=2023&paginatorType=Standard','https://lubimyczytac.pl/top100?page=2&listId=listTop100&month=5&year=2023&paginatorType=Standard','https://lubimyczytac.pl/top100?page=3&listId=listTop100&month=5&year=2023&paginatorType=Standard','https://lubimyczytac.pl/top100?page=4&listId=listTop100&month=5&year=2023&paginatorType=Standard','https://lubimyczytac.pl/top100?page=5&listId=listTop100&month=5&year=2023&paginatorType=Standard','https://lubimyczytac.pl/top100?page=6&listId=listTop100&month=5&year=2023&paginatorType=Standard','https://lubimyczytac.pl/top100?page=7&listId=listTop100&month=5&year=2023&paginatorType=Standard']
# Actual program:
# time.sleep(3)

driver.get(url)

# time.sleep(3)


#Check how many pages there is

num_of_next_pages = int(driver.find_element(By.XPATH,'//*[@id="buttonPaginationListP"]/li[3]/span').text)
if limitLinks:
    num_of_next_pages = 5
page_num = 0

while num_of_next_pages > page_num:

    driver.get(urls[page_num])
    # Find all the links to teams within the table rows
    books_links = driver.find_elements(By.CLASS_NAME, 'authorAllBooks__singleTextTitle')
    books_links_hrefs = [link.get_attribute('href') for link in books_links]

    print("Links:", books_links_hrefs),

    for url2 in books_links_hrefs:
        driver.get(url2)

        book_name = driver.find_element(By.XPATH, '//*[@id="book-info"]/div/h1').text
        type = driver.find_element(By.XPATH, '//*[@id="container-book"]/div/div[2]/div[1]/div[2]/a').text
        if len(driver.find_elements(By.XPATH, '//*[@id="container-book"]/div/div[2]/div[1]/div[2]/div[3]/span[1]'))>0:
            pages_num = driver.find_element(By.XPATH, '//*[@id="container-book"]/div/div[2]/div[1]/div[2]/div[3]/span[1]').text
        rating = driver.find_element(By.XPATH, '/html/body/div[5]/main/div/section[1]/div/div[3]/section[1]/div[1]/div[1]/span').text

        book_info = {'book_name': book_name, 'type': type, 'pages_num': pages_num.replace('str.', ''), 'rating': rating}
        books_df = books_df._append(book_info, ignore_index=True)

    page_num = page_num+1

print(books_df)
driver.quit()
