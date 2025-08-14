from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from bs4.element import Tag
import pandas as pd

SOURCE_URL: str = 'https://political-science.uchicago.edu'
MENUS: list = ['/people/department-leadership', 
               '/people/faculty', 
               '/people/faculty-associates', 
               '/people/emeriti', 
               '/people/lecturers', 
               '/people/PHDs-on-the-market', 
               '/people/staff',
               '/people/students', 
               '/people/instructional-associates']

data: list = []
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

for menu in MENUS:    
    current_link: str = SOURCE_URL + menu
    driver.get(current_link)
        
    while True:
        parser = BeautifulSoup(driver.page_source, 'html.parser')
        
        for person in parser.find_all('div', class_='views-row'):
            name_tag: Tag = person.find('h2', class_='no-tags')
            name: str = name_tag.get_text(strip=True) if name_tag else ''

            title_tag: Tag = person.find('div', class_='bio-subtitle')
            title: str = title_tag.get_text(strip=True) if title_tag else ''

            email_tag: Tag = person.find('div', class_='bio-email')
            email: str = email_tag.find('a').get_text(strip=True) if email_tag else ''

            data.append({
                'name': name,
                'title': title,
                'email': email,
            })

        next_button = parser.find('li', class_='pager__item--next')
        
        if not next_button:
            break
        
        next_link: str = current_link + next_button.find('a')['href']
        driver.get(next_link)

driver.quit()

df = pd.DataFrame(data)
df.to_csv('../data/output/uchicago_polsci.csv', index=False)
print('Data successfully written to CSV')