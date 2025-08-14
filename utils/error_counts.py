import pandas as pd
import re

# Path to your CSV
file_path = './data/r1_universities_output.csv'

# Load the CSV
df = pd.read_csv(file_path)

# Count total cells
total_cells = df.shape[0] * df.shape[1]

# Regex to match "INVALID: <number>"
pattern = re.compile(r'INVALID:\s*(\d+)')

# Dictionary to count errors
error_counts = {}

# Loop through each cell
for col in df.columns:
    for val in df[col].astype(str):
        match = pattern.search(val)
        if match:
            code = match.group(1)
            error_counts[code] = error_counts.get(code, 0) + 1

# Convert to DataFrame for nicer display
error_counts_df = pd.DataFrame(
    sorted(error_counts.items(), key=lambda x: x[1], reverse=True),
    columns=['Error Code', 'Count']
)

print(f"Total number of cells: {total_cells}")
print("\nError counts by code:")
print(error_counts_df)
