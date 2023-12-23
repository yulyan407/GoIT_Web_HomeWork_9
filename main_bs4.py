import json

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('span', class_='text')
authors = soup.find_all('small', class_='author')
author_details = soup.find_all('div', class_='quote')
tags = soup.find_all('div', class_='tags')
next_page = soup.find('li', class_='next')

while next_page:
    next_link = BASE_URL + next_page.a['href']
    response = requests.get(next_link)
    soup = BeautifulSoup(response.text, 'lxml')
    [quotes.append(q) for q in soup.find_all('span', class_='text')]
    [authors.append(a) for a in soup.find_all('small', class_='author')]
    [author_details.append(ad) for ad in soup.find_all('div', class_='quote')]
    [tags.append(t) for t in soup.find_all('div', class_='tags')]
    next_page = soup.find('li', class_='next')

quotes_data = []
author_links = []
for i in range(0, len(quotes)):
    quote_data = dict()
    quote_data["quote"] = quotes[i].text
    quote_data["author"] = authors[i].text
    quote_data["tags"] = []
    tags_for_quote = tags[i].find_all('a', class_='tag')
    for tag_for_quote in tags_for_quote:
        quote_data["tags"].append(tag_for_quote.text)
    quotes_data.append(quote_data)
    author_links.append(author_details[i].a['href'])


authors_data = []
for author in set(author_links):
    author_data = dict()
    author_link = BASE_URL + author
    a_response = requests.get(author_link)
    a_soup = BeautifulSoup(a_response.text, 'lxml')
    fullname = a_soup.find('h3', class_='author-title').text
    born_date = a_soup.find('span', class_='author-born-date').text
    born_location = a_soup.find('span', class_='author-born-location').text
    description = a_soup.find('div', class_='author-description').text
    author_data["fullname"] = fullname.strip()
    author_data["born_date"] = born_date.strip()
    author_data["born_location"] = born_location.strip()
    author_data["description"] = description.strip()
    authors_data.append(author_data)


with open('quotes_bs4.json', 'w', encoding='utf-8') as fd:
    json.dump(quotes_data, fd, ensure_ascii=False, indent=2)

with open('authors_bs4.json', 'w', encoding='utf-8') as fd:
    json.dump(authors_data, fd, ensure_ascii=False, indent=2)

