import requests
from urllib.parse import urlparse, ParseResult
import pandas as pd
import ast

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'en-US,en;q=0.5',
           'Referer': 'https://www.google.com/',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1'}

session = requests.Session()
session.headers.update(HEADERS)

df = pd.read_csv('./data/r1_universities.csv', na_values="['NA']")

def get_status_code(url: str) -> int:
    try:
        result: ParseResult = urlparse(url)
        if not all([result.scheme, result.netloc, result.path]):
            raise AttributeError
        
        response = session.get(url, allow_redirects=True, timeout=10)
        return response.status_code
    
    except Exception as err:
        pass
    return 500

def is_valid_url(url: str) -> bool:
    return get_status_code(url) < 400

for index, row in df.iterrows():
    print(f'Finished row {index}')
    
    for col, value in row.items():
        # print(f'Row: {index}, {col.title()}, {value}')
        if not isinstance(value, str):
            continue
        
        url_list: list = ast.literal_eval(value)
        
        if col.lower() == 'university':
            df.at[index, col] = url_list[0]
        else:
            noted_urls: list = []
            
            for url in url_list:
                result: int = get_status_code(url)
                
                if result >= 400:
                    # print(f'\tResult: {result}')
                    noted_urls.append(f'INVALID: {result}')
                
                noted_urls.append(url)
            df.at[index, col] = noted_urls
    
df.to_csv('./data/r1_universities_output.csv', index=False)
print('Data successfully written to CSV')