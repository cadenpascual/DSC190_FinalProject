import os
import csv
import requests
from bs4 import BeautifulSoup
all_rows = []

for i in range(1, 6):
    url = f"https://example.com/data/page/{i}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    data_items = soup.find_all('div', class_='data-item')
    for item in data_items:
        title = item.find('h2').text
        description = item.find('p').text
        print(f"Title: {title}\nDescription: {description}\n") 