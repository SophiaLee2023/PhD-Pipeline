from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from bs4.element import Tag
import pandas as pd

SOURCE_URL: str = 'https://www.american.edu/cas/biology/faculty.cfm'

data: list = []
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(SOURCE_URL)

parser = BeautifulSoup(driver.page_source, 'html.parser')

for person in parser.find_all('article', class_='profile-item'):
    name_tag: Tag = person.find('span', itemprop='name')
    name: str = name_tag.get_text(strip=True) if name_tag else ''

    title_tag: Tag = person.find('small', itemprop='jobTitle')
    title: str = title_tag.get_text(strip=True) if title_tag else ''

    email_tag: Tag = person.find('span', itemprop='email')
    email: str = email_tag.get_text(strip=True) if email_tag else ''

    data.append({
        'name': name,
        'title': title,
        'email': email,
    })
    print(name, title, email)

driver.quit()

df = pd.DataFrame(data)
df.to_csv('./data/output/americanu_biology.csv', index=False)
print('Data successfully written to CSV')