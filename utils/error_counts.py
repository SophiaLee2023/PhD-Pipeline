import pandas as pd
import re
from collections import defaultdict, Counter

# === Load CSV ===
file_path = './data/r1_universities_output.csv'
df = pd.read_csv(file_path)

# Regex to match "INVALID: <number>"
pattern = re.compile(r'INVALID:\s*(\d+)')

# ---- Overall error counts ----
overall_error_counts = defaultdict(int)

# ---- Row & column error tracking ----
row_error_counts = defaultdict(int)
row_error_breakdown = defaultdict(Counter)

col_error_counts = defaultdict(int)
col_error_breakdown = defaultdict(Counter)

# ---- Count filled cells (excluding first column & first row) ----
filled_cells_count = 0

# Map original row order (excluding header row)
row_order_map = {}
for r_idx, row in df.iterrows():
    row_id = row.iloc[0]
    row_order_map[row_id] = r_idx  # preserves natural order

# Map original column order (excluding first column)
col_order_map = {col: idx for idx, col in enumerate(df.columns)}

# ---- Loop through data ----
for r_idx, row in df.iterrows():
    row_id = row.iloc[0]  # First column value as identifier
    for col_idx, col in enumerate(df.columns):
        if r_idx == 0 or col_idx == 0:
            continue  # Skip first row and first column

        val_str = str(row[col])
        if val_str.strip() != "" and val_str.lower() != "nan":
            filled_cells_count += 1

        match = pattern.search(val_str)
        if match:
            code = match.group(1)

            # Overall counts
            overall_error_counts[code] += 1

            # Row-level
            row_error_counts[row_id] += 1
            row_error_breakdown[row_id][code] += 1

            # Column-level
            col_error_counts[col] += 1
            col_error_breakdown[col][code] += 1

# ---- Overall error DataFrame (sort by count) ----
overall_df = pd.DataFrame(
    sorted(overall_error_counts.items(), key=lambda x: x[1], reverse=True),
    columns=['Error Code', 'Count']
)

# ---- Get all unique error codes in appearance order from overall_df ----
all_error_codes = list(overall_df['Error Code'])

# ---- Row breakdown DataFrame (original CSV order) ----
row_data = []
for rid in sorted(row_error_counts, key=lambda x: row_order_map[x]):
    row_dict = {'Row ID (First Column)': rid, 'Total Error Count': row_error_counts[rid]}
    for code in all_error_codes:
        row_dict[f'num_error_{code}'] = row_error_breakdown[rid][code]
    row_data.append(row_dict)
row_df = pd.DataFrame(row_data)

# ---- Column breakdown DataFrame (original CSV order) ----
col_data = []
for cname in sorted(col_error_counts, key=lambda x: col_order_map[x]):
    col_dict = {'Column Name': cname, 'Total Error Count': col_error_counts[cname]}
    for code in all_error_codes:
        col_dict[f'num_error_{code}'] = col_error_breakdown[cname][code]
    col_data.append(col_dict)
col_df = pd.DataFrame(col_data)

# ---- Save outputs ----
overall_df.to_csv('./data/error_counts_overall.csv', index=False)
row_df.to_csv('./data/error_counts_by_row.csv', index=False)
col_df.to_csv('./data/error_counts_by_column.csv', index=False)

print(f"Number of filled cells (excluding first row & column): {filled_cells_count}")
print("Saved:")
print(" - ./data/error_counts_overall.csv")
print(" - ./data/error_counts_by_row.csv")
print(" - ./data/error_counts_by_column.csv")
