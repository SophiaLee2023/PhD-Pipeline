from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import ast

def export_errors(output_path: str) -> None:
    data: list = []
    df = pd.read_csv('./data/r1_universities_annotated.csv')

    for row in df.itertuples(index=False):
        for col, value in zip(df.columns, row):        
            if not isinstance(value, str) or col.lower() == 'university':
                continue
            
            url_list: list = ast.literal_eval(value)
            index: int = 0
            
            while index < len(url_list):
                url: str = url_list[index] 
                
                if 'invalid' in url.lower():
                    data.append((url[-3:], url_list[index + 1]))
                    index += 2
                else:
                    index += 1

    df_long = pd.DataFrame(data, columns=['error', 'url'])

    df_wide = df_long.pivot_table(index=df_long.groupby('error').cumcount(),
                                columns='error',
                                values='url',
                                aggfunc='first')
    df_wide = df_wide.reset_index(drop=True)

    df_wide.to_csv(output_path, index=False)
    print('Data successfully written to CSV')

def display_pages(input_path: str) -> None:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_page_load_timeout(5)

    df = pd.read_csv(input_path)

    for col in df.columns:
        print(f'Finished column: {col}')
        
        for index, value in df[col].items():
            if not isinstance(value, str):
                continue

            driver.get(f'{value}#error-code:{col}')

    driver.quit()
    
# export_errors('./data/links_by_error.csv')
display_pages('./data/links_by_error.csv')