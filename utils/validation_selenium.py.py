from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, ParseResult

import pandas as pd
import json
import ast

chrome_options = Options()
chrome_options.add_argument("--headless=chrome")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.set_page_load_timeout(5)

df = pd.read_csv('./data/r1_universities.csv', na_values="['NA']")

def get_status_code(logs: list, url: str) -> int:
    try:
        for entry in logs:
            msg = json.loads(entry['message'])
            response = msg.get('params', {}).get('response', {})

            if msg.get('method') == 'Network.responseReceived' and urlparse(response['url']).netloc == urlparse(url).netloc:
                return response.get('status')

    except: pass
    return 404

def is_valid_url(url: str) -> bool:
    try:
        result: ParseResult = urlparse(url)
        if not all([result.scheme, result.netloc, result.path]):
            raise AttributeError
        
        driver.get(url)
        logs: list = driver.get_log('performance')
        return get_status_code(logs, url) < 400
    
    except Exception as err:
        print(f'\t{err}')    
    return False

for index, row in df.iterrows():
    for col, value in row.items():
        print(f'Row: {index}, {col.title()}, {value}')
        
        if not isinstance(value, str):
            continue
        
        noted_urls: list = []
        
        for url in ast.literal_eval(value):
            if not is_valid_url(url):
                noted_urls.append('INVALID')
            
            # print(f'\tValid URL: {is_valid_url(url)}')
            noted_urls.append(url)

        df.at[index, col] = str(noted_urls)

# url1: str = 'https://agriculture.auburn.edu/directory/'
# url2: str = 'https://www.engr.colostate.edu/sbme/directory'
# url3: str = 'https://political-science.uchicago.edu/people/department-leadership'
# print(is_valid_url(url3))

driver.quit()
    
df.to_csv('./data/r1_universities_clean.csv', index=False)
print('Data successfully written to CSV')