from urllib import request
from bs4 import BeautifulSoup as BS
import pandas as pd
import time
import matplotlib.pyplot as plt

# Start
start = time.time()

limitLinks = True

# Limiting the range: for limitLinks = True, the first 5 pages are scrapped, each containing 20 books
if limitLinks:
    pages = range(1, 6)
else:
    pages = range(1, 8)

# Scraping links for each book
base_url = 'https://lubimyczytac.pl/top100?page={}&listId=listTop100&month=5&year=2023&paginatorType=Standard'

books_links = []

for page in pages:
    url = base_url.format(page)
    html = request.urlopen(url)
    bs = BS(html.read(), 'html.parser')

    tags = bs.find_all('a', {'class': 'authorAllBooks__singleTextTitle float-left'})

    for tag in tags:
        books_links.append('https://lubimyczytac.pl' + tag['href'])

a = pd.DataFrame({'Links': books_links})
print(a)

# # Saving to csv file
a.to_csv('books_links.csv')

# Scraping title, pages, rating and category for each book

b = pd.DataFrame({'book_name': [], 'pages_num': [], 'rating': [],'type': []})

for link in books_links:

    html = request.urlopen(link)
    bs = BS(html.read(), 'html.parser')

    try:
        book_name = bs.find('h1', {'class': 'book__title'}).get_text()
    except:
        book_name = ''

    try:
        pages_num = bs.find('span', {'class': 'd-sm-inline-block book-pages book__pages pr-2 mr-2 pr-sm-3 mr-sm-3'}).get_text()
        pages_num = pages_num.replace('str.', '')
    except:
        pages_num = ''

    try:
        rating = bs.find('section', {'class': 'container book'}).find('span', {'class': 'big-number'}).get_text()
        rating = rating.replace(',', '.')
    except:
        rating = ''

    try:
        type = bs.find('a', {'class': 'book__category d-sm-block d-none'}).get_text()
    except:
        type = ''

    books = {'book_name': book_name,'pages_num': pages_num,'rating':rating, 'type': type}
    b = b._append(books, ignore_index=True)
    print(b)

# # Saving to csv file
b.to_csv('books_data.csv')

# End
end = time.time()
print("Beautiful Soup time:", end - start, "s")



## Pie chart

df =  pd.read_csv('books_data.csv')
category_data = df["type"]
category_counts = category_data.value_counts()
print('Number of categories:', category_counts.count())
categories = category_counts.index.tolist()
counts = category_counts.values.tolist()
colors = plt.cm.tab20(range(len(categories)))
explode = (0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25)
plt.pie(counts, colors=colors, autopct='%1.1f%%', pctdistance=0.85, shadow=True, startangle=200, explode=explode, textprops={'fontsize': 9})
legend = plt.legend(categories, loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=3, prop={'size': 6.8})
plt.title("Categories")
plt.axis('equal')
plt.ylabel('')
plt.show()

