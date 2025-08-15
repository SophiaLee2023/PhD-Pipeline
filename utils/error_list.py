import pandas as pd
import ast

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

df_wide.to_csv('./data/links_by_error.csv', index=False)
print('Data successfully written to CSV')