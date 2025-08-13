from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

SOURCE = 'http://quotes.toscrape.com/'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(SOURCE)

data = list()

while True:
    parser = BeautifulSoup(driver.page_source, 'html.parser')
    quotes = parser.find_all('div', class_='quote')

    if not quotes:
        break

    for quote in quotes:
        description = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        
        data.append({'author': author, 'quote': description})

    next_link = parser.find('li', class_='next')

    if not next_link:
        break

    next_page_url = next_link.find('a')['href']

    if not next_page_url.startswith('http'):
        next_page_url = SOURCE + next_page_url

    driver.get(next_page_url)

driver.quit()

df = pd.DataFrame(data)
df.to_csv('./output.csv', index=False)
print(f'All data has been written')