from urllib import request
from bs4 import BeautifulSoup as BS
import pandas as pd
import re
import time
import matplotlib.pyplot as plt
import numpy as np


# Start of scrapping
start = time.time()

limitLinks = False

# Limiting the range: for limitLinks = True, first 5 pages are scrapped, each containing 20 books.
if limitLinks:
    RANGE = range(1, 6)
else:
    RANGE = range(1,8)

# Scrapping links for each book
base_url = 'https://lubimyczytac.pl/top100?page={}&listId=listTop100&month=5&year=2023&paginatorType=Standard'

book_links = []

for page in RANGE:
    url = base_url.format(page)
    html = request.urlopen(url)
    bs = BS(html.read(), 'html.parser')

    tags = bs.find_all('a', {'class': 'authorAllBooks__singleTextTitle float-left'})

    for tag in tags:
        book_links.append('https://lubimyczytac.pl' + tag['href'])

a = pd.DataFrame({'Link': book_links})
print(a)

# Saving to csv file
a.to_csv('book_links.csv')

# Scrapping title, pages, rating and category for each book

b = pd.DataFrame({'title': [], 'pages': [], 'rating': [],'category': []})

for link in book_links:

    html = request.urlopen(link)
    bs = BS(html.read(), 'html.parser')

    try:
        title = bs.find('h1', {'class': 'book__title'}).get_text()
    except:
        title = ''

    try:
        pages = bs.find('span', {'class': 'book__pages'}).get_text()
        pages = pages.replace('str.', '')
    except:
        pages = ''

    try:
        rating = bs.find('span', {'class': 'big-number'}).get_text()
        rating = rating.replace(',', '.')
    except:
        rating = ''

    try:
        category = bs.find('a', {'class': 'book__category'}).get_text()
    except:
        category = ''

    books = {'title': title,'pages': pages,'rating':rating, 'category': category}
    b = b._append(books, ignore_index=True)
    print(b)

# Saving to csv file
b.to_csv('book_data.csv')

# End of scrapping
end = time.time()
print("BeautifulSoup time:", end - start, "s")

## Pie chart

df =  pd.read_csv('book_data.csv')
category_data = df["category"]
category_counts = category_data.value_counts()
print(category_counts.count())
categories = category_counts.index.tolist()
counts = category_counts.values.tolist()
colors = plt.cm.Set3(range(len(categories)))
explode = (0, 0, 0, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4, 0.4, 0.5)
plt.pie(counts, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140, explode=explode)
plt.legend(categories, loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3)
plt.title("Distribution of Categories")
plt.axis('equal')
plt.ylabel('')
plt.show()
